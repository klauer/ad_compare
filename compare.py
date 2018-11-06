import pathlib
import pandas as pd
from recordwhat.parsers.db_parsimonious import dbWalker, db_grammar


def strip_quotes(text):
    return text.strip('\'"')


versions = [
    'R1-9-1',
    'R2-0',
    'R2-1',
    'R2-2',
    'R2-3',
    'R2-4',
    'R2-5',
    'R2-6',
    'R3-1',
    'R3-2',
    'R3-3',
    'R3-3-1',
    'R3-3-2',
]


filenames = [
    'ADBase.template',
    'ADPrefixes.template',
    'NDColorConvert.template',
    'NDFile.template',
    'NDFileHDF5.template',
    'NDFileJPEG.template',
    'NDFileMagick.template',
    'NDFileNetCDF.template',
    'NDFileNexus.template',
    'NDFileTIFF.template',
    'NDOverlay.template',
    'NDOverlayN.template',
    'NDPluginBase.template',
    'NDProcess.template',
    'NDROI.template',
    'NDROI_sync.template',
    'NDStats.template',
    'NDStdArrays.template',
    'NDTransform.template',
]


simple_changes = [
    ('$(ADDR)', '$(ADDR=0)'),
    ('$(TIMEOUT)', '$(TIMEOUT=1)'),
]


def summarize_record_info(db_text):
    parsed = db_grammar.parse(db_text)
    walker = dbWalker()
    record_info = {}

    for i, item in enumerate(sorted(walker.visit(parsed),
                                    key=lambda item: item.pvname)):
        pvname = strip_quotes(item.pvname)
        if pvname.startswith('$(P)$(R)'):
            pvname = pvname[len('$(P)$(R)'):]

        info = [f'RTYP {item.rtype}']
        for field_name, field in sorted(item.fields.items()):
            value = strip_quotes(field.value)
            info.append(f'{field_name} f{value}')
        for field_name, field in sorted(item.info.items()):
            value = strip_quotes(field.value)
            info.append(f'INFO: {field_name} f{value}')

        record_info[pvname] = '\n'.join(info)

    return record_info


def undo_changes(value, change_list):
    for from_, to in change_list:
        value = value.replace(to, from_)
    return value


def preprocess(db_text):
    'Pre-process the DB text due to some failures in the grammar of recordwhat'
    lines = []
    for line in db_text.split('\n'):
        line = line.strip()
        if line.startswith('field(') or line.startswith('info('):
            orig_line = line
            field, value = line.split(',', 1)
            start, field = field.split('(', 1)
            field = field.strip('"')
            # strip off the final )
            value = value[:-1]
            value = value.strip(' ').strip('"')
            # TODO default string values
            value = value.replace('=""', '')
            line = f'{start}({field}, "{value}")'
            # if orig_line != line:
            #     print('fixed', orig_line, '->', line)
        lines.append(line)
    # print('\n'.join(lines))
    return '\n'.join(lines)


def compare(fn, *, ignore_simple_changes=True):
    version_info = {}
    for version in versions:
        full_fn = pathlib.Path(version) / 'ADApp/Db' / fn
        print(full_fn)
        try:
            with open(full_fn) as f:
                db_text = f.read()
        except FileNotFoundError:
            version_info[version] = {}
            continue

        db_text = preprocess(db_text)
        version_info[version] = summarize_record_info(db_text)

    df = pd.DataFrame.from_dict(version_info)
    df = df.fillna('n/a')

    for pvname in df.index:
        initial_value = df.at[pvname, versions[0]]
        for version in versions[1:]:
            value = df.at[pvname, version]

            if ignore_simple_changes:
                value = undo_changes(value, simple_changes)

            if value == initial_value:
                if initial_value == 'n/a':
                    df.at[pvname, version] = 'n/a'
                else:
                    df.at[pvname, version] = 'same'
            elif value.startswith(initial_value):
                df.at[pvname, version] = 'added:\n' + value[len(initial_value):]
                initial_value = value
            else:
                initial_value = value

    return df


def html_formatter(s):
    return s.replace('\n', '<br>')


def main(comparison_fn):
    old_width = pd.get_option('display.max_colwidth')
    pd.set_option('display.max_colwidth', -1)

    with open(comparison_fn, 'wt') as f:
        print(f'<html><head></head>', file=f)
        print(f'<body>', file=f)
        for fn in filenames:
            df = compare(fn)
            html_comparison = df.to_html(
                formatters=[html_formatter] * len(versions),
                escape=False)

            print(f'<h1>{fn}</h1>', file=f)
            print(html_comparison, file=f)
        print(f'</body>', file=f)
    pd.set_option('display.max_colwidth', old_width)


if __name__ == '__main__':
    main('index.html')
