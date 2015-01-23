from lib.HTML_form_parser import HTMLFormParser

simpleWebContent = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Table</title>
</head>
<body>
    <table border="1">
    <tbody>
        <tr>
            <th>This</th>
            <th>is</th>
            <th>header</th>
        </tr>
        <tr>
            <td>This</td>
            <td>is</td>
            <td>content</td>
        </tr>
    </tbody>
    </table>
</body>
</html>
'''


def test_getHeader_with_simpleWebContent():
    parser = HTMLFormParser()
    for line in simpleWebContent.splitlines():
        parser.feed(line)
    assert parser.get_header() == ['This', 'is', 'header']


def test_getTable_with_simpleWebContent():
    parser = HTMLFormParser()
    for line in simpleWebContent.splitlines():
        parser.feed(line)
    assert parser.get_table() == [['This', 'is', 'header'],
                                  ['This', 'is', 'content']]


def test_getContent_with_simpleWebContent():
    parser = HTMLFormParser()
    for line in simpleWebContent.splitlines():
        parser.feed(line)
    assert parser.get_content() == [['This', 'is', 'content']]
