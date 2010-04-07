from ptemplate.ctemplate import CTemplate

data = {
    "SEC": [{}],
    "SUBSEC": [{}],
}
input = "boo!hi {{#SEC}}lo{{#SUBSEC}}jo{{/SUBSEC}}{{/SEC}} bar"
template = CTemplate(input)
output = "boo!hi lojo bar"
tokens = template.formatter.tokenize(template.preprocessor(template.template))
print "tokens:"
print '\n'.join("\t" + repr(x) for x in tokens)

print
print "data:\t", repr(data)
print "input:\t", repr(input)
print "output:\t", repr(output)
result = template.render(**data)
print "result:\t%s (%s)" % (repr(result), result == output and "" or "BAD")
