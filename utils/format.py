def format_example(ex):
    if "->" not in ex:
        return "<li>" + ex + "</li>"

    from_l = ex.split(" -> ")[0]
    to_l = ex.split(" -> ")[1]
    return "<li> <em>" + from_l + "</em>  &#8594;  " + to_l + "</li>"


def format_examples(examples):
    if len(examples) == 0:
        return ''

    html = "<h2>Ejemplos:</h2>"
    html = html + "<ul>"
    for ex in examples:
        html = html + format_example(ex)
    return html + "</ul>"


def format_meaning(m):
    if '(' in m:
        return "<li> <em>" + m[1:-1] + "</em> </li>"
    else:
        return "<li> " + m + " </li>"


def format_sense(sense):
    if len(sense.meanings) == 0:
        return ''

    html = "<h2>Sentido:</h2>"
    html = html + "<ul>"
    for m in sense.meanings:
        html = html + format_meaning(m)
    return html + "</ul>"


def format_senses(result):
    html = ""
    for sense in result.senses:
        html = html + format_sense(sense) + format_examples(sense.examples)
        if html:
            html = html + "<hr>"

    return html


def format_sound(path):
    if not path:
        return ''

    return '[sound:' + path + ']' + \
           "<audio controls>" + "<source src=\"" + path + "\" type=\"audio/mpeg\">" + \
           "Not supported" + "</audio>"
