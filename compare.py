import os
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


grouped_filenames = [
    ('ADBase.template', 'NDArrayBase.template'),
]

skipped_filenames = set(
    # TODO: new (?) "substitute" syntax
    ('NDROIStat8.template',
     )
)


simple_changes = [
    ('$(ADDR)', '$(ADDR=0)'),
    ('$(TIMEOUT)', '$(TIMEOUT=1)'),
    ('PINI NO', 'PINI YES'),
    ('PINI YES', 'PINI NO'),
]

header = '''
<html>
<head>
<style>
table {
    border-collapse: collapse;
    width: 100%;
}

th, td {
    text-align: center;
    padding: 8px;
}

tr:nth-child(even) {
    background-color: #f2f2f2;
}
</style>
</head>
<body>
<h1>Notes</h1>
This compares what PVs are available from each version of AreaDetector.<br/>
<br/>
Special meanings:<br/>
NO - PV does not exist in the specific version<br/>
"-" - PV is the same as the previous version<br/>
<h1>Index</h1>
'''


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
            info.append(f'{field_name} {value}')
        for field_name, field in sorted(item.info.items()):
            value = strip_quotes(field.value)
            info.append(f'INFO: {field_name} {value}')

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
            # orig_line = line
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


def compare(fns, *, ignore_simple_changes=True):
    version_info = {}
    if isinstance(fns, str):
        fns = (fns, )
    for version in versions:
        db_text = []
        for fn in fns:
            full_fn = pathlib.Path(version) / 'ADApp' / 'Db' / fn
            print(full_fn)
            try:
                with open(full_fn) as f:
                    db_text.append(f.read())
            except FileNotFoundError:
                version_info[version] = {}

        db_text = '\n'.join(db_text)
        if not db_text:
            continue

        db_text = preprocess(db_text)
        version_info[version] = summarize_record_info(db_text)

    df = pd.DataFrame.from_dict(version_info)
    missing = 'NO'
    df = df.fillna(missing)

    for pvname in df.index:
        initial_value = df.at[pvname, versions[0]]
        for version in versions[1:]:
            value = df.at[pvname, version]

            if ignore_simple_changes:
                value = undo_changes(value, simple_changes)

            if value == initial_value:
                if initial_value == missing:
                    df.at[pvname, version] = missing
                else:
                    df.at[pvname, version] = '-'
            elif value.startswith(initial_value):
                df.at[pvname, version] = (
                    'added:\n' + value[len(initial_value):].strip('\n ')
                )
                initial_value = value
            else:
                initial_value = value

    return df


def find_templates():
    ignore = set(fn
                 for fns in grouped_filenames
                 for fn in fns)
    ignore = ignore.union(skipped_filenames)

    fns = set()
    for version in versions:
        version_fns = [
            fn for fn in
            os.listdir(pathlib.Path(version) / 'ADApp' / 'Db')
            if fn.endswith('.template')
        ]

        for fn in version_fns:
            print(fn, ignore)
            if fn not in ignore:
                fns.add(fn)

    return grouped_filenames + list([fn] for fn in sorted(fns))


def html_formatter(s):
    return s.replace('\n', '<br/>')


def main(comparison_fn):
    old_width = pd.get_option('display.max_colwidth')
    pd.set_option('display.max_colwidth', -1)

    with open(comparison_fn, 'wt') as f:
        print(header, file=f)

        def title_from_fns(fns):
            return ' + '.join(fns)

        for idx, fns in enumerate(find_templates()):
            title = title_from_fns(fns)
            print(f'<li><a href="#{idx}">{title}</li>', file=f)

        for idx, fns in enumerate(find_templates()):
            df = compare(fns)
            html_comparison = df.to_html(
                formatters=[html_formatter] * len(versions),
                escape=False)

            title = title_from_fns(fns)
            print(f'<h1><a name={idx}>{title}</a></h1>', file=f)
            print(html_comparison, file=f)
        print(f'</body>', file=f)
    pd.set_option('display.max_colwidth', old_width)


if __name__ == '__main__':
    main('docs/index.html')
