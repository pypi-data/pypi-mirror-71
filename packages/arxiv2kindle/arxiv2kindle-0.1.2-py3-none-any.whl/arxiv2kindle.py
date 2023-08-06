#!/usr/bin/env python3

import argparse
import requests
import lxml.html as html
import logging
import re
import os
import sys
import subprocess
import tempfile
import tarfile
from pathlib import Path


DEFAULT_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) "
              "Gecko/20100101 Firefox/21.0")
ARXIV_REGEX = r'(https?://.*?/)?(?P<id>\d{4}\.\d{4,5}(v\d{1,2})?)'


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

HELP_EPILOG = """\
Example usage:

  %(prog)s --width 4 --height 6 --margin 0.2 https://arxiv.org/abs/1802.08395 > out.pdf
  %(prog)s --width 6 --height 4 --margin 0.2 --landscape --dest-dir ./ https://arxiv.org/abs/1802.08395
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert arxiv paper to kindle-like size",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=HELP_EPILOG
        )
    parser.add_argument("query", help="arxiv paper url")
    group = parser.add_argument_group("Geometry")
    group.add_argument(
        '-W', "--width", default=4, type=float,
        help="width of the output pdf (inches)")
    group.add_argument(
        '-H', "--height", default=6, type=float,
        help="height of the output pdf (inches)")
    group.add_argument(
        '-m', "--margin", default=0.2, type=float,
        help="margin for the output pdf (inches)")
    group.add_argument(
        "--landscape", action='store_true',
        help="produce a landscape file")
    group.add_argument(
        "--portrait", dest='landscape', action='store_false',
        help="produce a portrait file (default option)")
    parser.add_argument(
        "--user-agent", default=DEFAULT_UA,
        help="user agent to use for downloading the paper")
    parser.add_argument(
        "--dest-dir", type=Path, default=None,
        help="destination dir, if none provided, the file is streamed to stdout"
    )
    args = parser.parse_args()
    return args


def download(query, user_agent):
    arxiv_id = re.match(ARXIV_REGEX, query).group('id')
    arxiv_abs = 'http://arxiv.org/abs/' + arxiv_id
    arxiv_pdf = 'http://arxiv.org/pdf/' + arxiv_id
    arxiv_pgtitle = html.fromstring(
        requests.get(arxiv_abs).text.encode('utf8')).xpath('/html/head/title/text()')[0]
    arxiv_title = re.sub(r'\s+', ' ', re.sub(r'^\[[^]]+\]\s*', '', arxiv_pgtitle), re.DOTALL)

    logger.info(f"Converting paper: [{arxiv_id}] {arxiv_title}")
    logger.info(f"Pdf link: {arxiv_pdf}")

    temp_dir = Path(tempfile.mkdtemp(prefix='arxiv2kindle_'))

    url = 'http://arxiv.org/e-print/' + arxiv_id
    logger.info(f"Downloading the source from {url}...")
    with open(temp_dir / 'src.tar.gz', 'wb') as f:
        r = requests.get(url, headers={'User-Agent': user_agent},
                         allow_redirects=True)
        assert r.status_code == 200
        f.write(r.content)

    logger.info(f'Extracting the source...')
    with tarfile.open(temp_dir / 'src.tar.gz') as f:
        f.extractall(temp_dir)

    def is_main_file(file_name):
        with open(file_name, 'rt') as f:
            if '\\documentclass' in f.read():
                return True
        return False

    main_files = [tex_file for tex_file in temp_dir.glob('*.tex')
                  if is_main_file(tex_file)]
    assert len(main_files) == 1
    main_file, = main_files
    logger.info(f'Fount the main tex file: {main_file.name}')
    return temp_dir, main_file, arxiv_title


def change_size(main_file, geom_settings, landscape):
    with open(main_file, 'rt') as f:
        src = f.readlines()

    # documentclass line index
    dclass_idx = next(idx for idx, line in enumerate(src)
                      if '\\documentclass' in line)

    # filter comments/newlines for easier debugging:
    src = [line for line in src if line[0] != '%' and len(line.strip()) > 0]

    # strip font size, column stuff, and paper size stuff in documentclass line:
    src[dclass_idx] = re.sub(r'\b\d+pt\b', '', src[dclass_idx])
    src[dclass_idx] = re.sub(r'\b\w+column\b', '', src[dclass_idx])
    src[dclass_idx] = re.sub(r'\b\w+paper\b', '', src[dclass_idx])
    # remove extraneous starting commas
    src[dclass_idx] = re.sub(r'(?<=\[),', '', src[dclass_idx])
    # remove extraneous middle/ending commas
    src[dclass_idx] = re.sub(r',(?=[\],])', '', src[dclass_idx])

    # find begin{document}:
    begindocs = [i for i, line in enumerate(src) if line.startswith(r'\begin{document}')]
    assert(len(begindocs) == 1)
    geom_settings_str = ",".join(k+"="+v for k, v in geom_settings.items())
    geom_settings_str += ",landscape" if landscape else ""
    src.insert(
        begindocs[0],
        f'\\usepackage[{geom_settings_str}]{{geometry}}\n')
    src.insert(begindocs[0], '\\usepackage{times}\n')
    src.insert(begindocs[0], '\\pagestyle{empty}\n')
    src.insert(begindocs[0], '\\usepackage{breqn}\n')
    if landscape:
        src.insert(begindocs[0], '\\usepackage{pdflscape}\n')

    # shrink figures to be at most the size of the page:
    for i in range(len(src)):
        line = src[i]
        m = re.search(r'\\includegraphics\[width=([.\d]+)\\(line|text)width\]', line)
        if m:
            mul = m.group(1)
            src[i] = re.sub(
                r'\\includegraphics\[width=([.\d]+)\\(line|text)width\]',
                f'\\\\includegraphics[width={mul}\\\\textwidth,height={mul}\\\\textheight,keepaspectratio]',
                line)
            continue
        # deal with figures which do not have sizes specified
        if '\\includegraphics{' in line:
            src[i] = re.sub(
                r'\\includegraphics{',
                r'\\includegraphics[scale=0.5]{',
                line)
            continue
        # deal with scaled figures
        m = re.search(r'\\includegraphics\[scale=([.\d]+)\]', line)
        if m:
            mul = float(m.group(1))
            src[i] = re.sub(
                r'\\includegraphics\[scale=([.\d]+)\]',
                f'\\\\includegraphics\\[scale={mul / 2}\\]',
                line)
            continue

    # allow placing inline equations on new line
    for i in range(len(src)):
        line = src[i]
        m = re.search(r'\$.+\$', line)
        if m:
            src[i] = "\\sloppy " + line

    os.rename(main_file, main_file.with_suffix('.tex.bak'))
    with open(main_file, 'wt') as f:
        f.writelines(src)


def compile_tex(file_name):
    # Compile 3 times
    for _ in range(3):
        subprocess.run(['pdflatex', file_name],
                       stdout=sys.stderr,
                       cwd=file_name.parent)


def rotate_pdf(pdf_file):
    os.rename(pdf_file, pdf_file.with_suffix('.pdf.bak'))
    subprocess.run(
        ['pdftk', pdf_file.with_suffix('.pdf.bak'),
         'rotate', '1-endeast', 'output', pdf_file],
        stdout=sys.stderr,
        cwd=pdf_file.parent)


def make_single_column(work_dir):
    for filename in work_dir.glob('*.sty'):
        with open(filename, 'rt') as f:
            src = f.readlines()
        out_src = []
        for line in src:
            if line.strip() == '\\twocolumn':
                continue
            out_src.append(line)
        with open(filename, 'wt') as f:
            f.writelines(out_src)


def check_prerec(landscape):
    result = subprocess.run(["pdflatex", "--version"], stdout=None, stderr=None)
    if result.returncode != 0:
        raise SystemError("no pdflatex found")
    if landscape:
        result = subprocess.run(["pdftk", "--version"], stdout=None, stderr=None)
        if result.returncode != 0:
            raise SystemError("no pdftk found (required for landscape mode)")


def main(query, width, height, margin, user_agent, landscape, dest_dir):
    check_prerec(landscape)
    
    tmp_dir, main_file, title = download(query, user_agent)
    if landscape:
        width, height = height, width
    geom_settings = dict(
        paperwidth=f'{width}in',
        paperheight=f'{height}in',
        margin=f'{margin}in')

    change_size(main_file, geom_settings, landscape)
    make_single_column(tmp_dir)
    compile_tex(main_file)
    pdf_file = main_file.with_suffix('.pdf')
    if landscape:
        rotate_pdf(pdf_file)

    if dest_dir is not None:
        os.rename(pdf_file, dest_dir / (title + '.pdf'))
    else:
        with open(main_file.with_suffix('.pdf'), 'rb') as fin:
            sys.stdout.buffer.write(fin.read())


def run():
    main(**vars(parse_args()))


if __name__ == "__main__":
    run()
