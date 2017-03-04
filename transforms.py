
import re

import utilities
import component
import postprocess
import myoperations
import mapping


###################

def mbx_fix(text):
    """ Correct some authoring shortcuts.

    """

    thetext = text

    # allow the user to omit the <main> in an index entry,
    # and to use LaTeX-style <index>theorem!three color</index>
    thetext = re.sub(r"<index>(.*?)</index>", index_fix, thetext, 0, re.DOTALL)

    return thetext

###################

def mbx_strict(text):
    """ Remove white space that confuses xslt.

    """

    # need a big comment explaining the general ideas, pluse one for each case

    thetext = text

    thetext = postprocess.tag_before_after("mrow|intertext", "\n", "", "", "\n", thetext)

    # do p and li separately, and in this order, because of p in li
    thetext = postprocess.tag_before_after("p", "x", "", "", "\n", thetext)
    thetext = postprocess.tag_before_after("li", "x", "", "", "\n", thetext)

    # no white space arounf me, md, etc
    thetext = postprocess.tag_before_after("md|mdn", "", "x", "x", "", thetext)
    thetext = postprocess.tag_before_after("me|men", "", "", "", "", thetext)

    return thetext

###################

def mbx_strict_tex(text):
    # Nothing here yet

    # need to worry about things like white space in paragraphs

    thetext = text

    return thetext

###################

def mbx_strict_html(text):
    """ Rewrite some markup that confuses HTML/MathJax.

    """

    thetext = text

    # mathjax can cause a line feed between math and punctuation
    thetext = re.sub("</m>\s*([,:;.!?\-\)'\"]+)\s+<m>", r"\\text{\1}</m><nbsp /><m>", thetext)
    thetext = re.sub("</m>\s*([,:;.!?\-\)'\"]+)", r"\\text{\1}</m>", thetext)

    # there can also be puntuation before math: (<m> x = 9 </m>)

    # where do we rearrange the punctuation for multi-line math?

    return thetext

###################

def mbx_fa(text):
    """ replace f(x) by \fa{f}{x}.

    """

    thetext = text

    # first process all of the inline math 
    thetext = re.sub(r"<m>.*?</m>", myoperations.fa_convert, thetext, 0, re.DOTALL)
    # and then the simple display math
    thetext = re.sub(r"<me>.*?</me>", myoperations.fa_convert, thetext, 0, re.DOTALL)
    thetext = re.sub(r"<men[^>]*>.*?</men>", myoperations.fa_convert, thetext, 0, re.DOTALL)
    # a row of a multiline
    thetext = re.sub(r"<mrow>.*?</mrow>", myoperations.fa_convert, thetext, 0, re.DOTALL)

    return thetext

###################

def mbx_pp(text):
    """ Pretty-print MBX source.

    """

    thetext = text

    # first a hack to handle 2-level lists.
    thetext = re.sub(r"<li>\s*<p>", "<lip>", thetext)
    thetext = re.sub(r"</p>\s*</li>", "</lip>", thetext)
    component.lipcounter = 0
    component.something_changed = True
    while component.something_changed:
        component.something_changed = False
        thetext = re.sub(r"<lip>(.*?)</lip>", liprename, thetext, 0, re.DOTALL)

#    print "found", component.lipcounter, "li/p pairs"
    for n in range(component.lipcounter):
        thetext = postprocess.tag_before_after("lip" + str(n), "\n\n", "\n", "\n", "\n\n", thetext)
    thetext = postprocess.tag_before_after("lip", "\n\n", "\n", "\n", "\n\n", thetext)

    # first remove extraneous spaces and put in appropriate carriage returns

    thetext = postprocess.tag_before_after("p", "\n\n", "\n", "\n", "\n\n", thetext)
    thetext = postprocess.tag_before_after("row|tabular|image|latex-image-code|asymptote", "\n", "\n", "\n", "\n", thetext)
    thetext = postprocess.tag_before_after("me|men|md|mdn", "\n", "\n", "\n", "\n", thetext)
    thetext = postprocess.tag_before_after("exercises|exercisegroup|exercise", "\n", "\n", "\n", "\n", thetext)
    thetext = postprocess.tag_before_after("webwork|setup|set|pg-code", "\n", "\n", "\n", "\n", thetext)
    thetext = postprocess.tag_before_after("mrow|intertext", "\n", "", "", "\n", thetext)
    thetext = postprocess.tag_before_after("dt", "\n\n", "", "", "\n", thetext)
    thetext = postprocess.tag_before_after("dd", "\n", "", "", "\n\n", thetext)
    thetext = postprocess.tag_before_after("li", "\n\n", "", "", "\n\n", thetext)
    thetext = postprocess.tag_before_after("ul|ol|dl", "\n", "\n", "\n", "\n", thetext)
    thetext = postprocess.tag_before_after("theorem|proposition|lemma|conjecture|corollary",
                                           "\n\n", "\n", "\n", "\n\n", thetext)
    thetext = postprocess.tag_before_after("algorithm",
                                           "\n\n", "\n", "\n", "\n\n", thetext)
    thetext = postprocess.tag_before_after("objectives",
                                           "\n\n", "\n", "\n", "\n\n", thetext)
    thetext = postprocess.tag_before_after("definition|axiom|example|insight|exploration|activity|remark|proof",
                                           "\n\n", "\n", "\n", "\n\n", thetext)
    thetext = postprocess.tag_before_after("problem", "\n\n", "\n", "\n", "\n\n", thetext)
    thetext = postprocess.tag_before_after("figure|table",
                                           "\n\n", "\n", "\n", "\n\n", thetext)
    thetext = postprocess.tag_before_after("paragraphs|sidebyside|aside", "\n\n", "\n", "\n", "\n", thetext)
    thetext = postprocess.tag_before_after("introduction|statement|solution|answer|hint|objectives", "\n", "\n", "\n", "\n", thetext)
    thetext = postprocess.tag_before_after("subsection", "\n\n", "\n", "\n", "\n\n", thetext)
    thetext = postprocess.tag_before_after("chapter|section", "\n", "\n", "\n", "\n", thetext)
    thetext = postprocess.tag_before_after("title|cell|caption", "\n", "", "", "\n", thetext)

#    # first remove all the spaces at the beginning of a line
#    thetext = re.sub("\n +", "\n", thetext)

    # then put it back
    for n in range(component.lipcounter):
        thetext = postprocess.add_space_within("lip" + str(n), thetext)
        thetext = postprocess.add_space_within("lip" + str(n), thetext)  # twice, because we will separate into li and p

    thetext = postprocess.add_space_within("chapter", thetext)
    thetext = postprocess.add_space_within("section", thetext)
    thetext = postprocess.add_space_within("subsection", thetext)
    thetext = postprocess.add_space_within("introduction", thetext)
    thetext = postprocess.add_space_within("objectives", thetext)
    thetext = postprocess.add_space_within("figure", thetext)
    thetext = postprocess.add_space_within("image", thetext)
    thetext = postprocess.add_space_within("asymptote", thetext)
    thetext = postprocess.add_space_within("sidebyside", thetext)
    thetext = postprocess.add_space_within("aside", thetext)
    thetext = postprocess.add_space_within("latex-image-code", thetext)
    thetext = postprocess.add_space_within("definition|axiom|theorem|example|insight|exploration|activity", thetext)
    thetext = postprocess.add_space_within("algorithm|objectives", thetext)
    thetext = postprocess.add_space_within("proposition|lemma|remark|conjecture|corollary", thetext)
    thetext = postprocess.add_space_within("statement|solution|answer|hint|proof", thetext)
    thetext = postprocess.add_space_within("p", thetext)
    thetext = postprocess.add_space_within("paragraphs", thetext)
    thetext = postprocess.add_space_within("ul", thetext)
    thetext = postprocess.add_space_within("ol", thetext)
    thetext = postprocess.add_space_within("dl", thetext)
    thetext = postprocess.add_space_within("li", thetext)
    thetext = postprocess.add_space_within("me|men|md|mdn", thetext)
    thetext = postprocess.add_space_within("exercises", thetext)
    thetext = postprocess.add_space_within("exercisegroup", thetext)
    thetext = postprocess.add_space_within("exercise", thetext)
    thetext = postprocess.add_space_within("problem", thetext)
    thetext = postprocess.add_space_within("webwork", thetext)
    thetext = postprocess.add_space_within("setup", thetext)
 #   thetext = postprocess.add_space_within("var", thetext)
    thetext = postprocess.add_space_within("set", thetext)
    thetext = postprocess.add_space_within("pg-code", thetext)
    thetext = postprocess.add_space_within("table", thetext)
    thetext = postprocess.add_space_within("tabular", thetext)
    thetext = postprocess.add_space_within("row", thetext)
    thetext = postprocess.add_space_within("pre", thetext)

    # now separate the li and p
    for n in range(component.lipcounter):
        thetext = re.sub(r"(\n *)  <lip" + str(n) + ">",r"\1  <li>\1    <p>", thetext)
        thetext = re.sub(r"(\n *)</lip" + str(n) + ">",r"\1  </p>\1</li>", thetext)
    # for some reason there can be extra </lip>.  Not sure why.
    thetext = re.sub(r"(\n *)</lip>",r"\1  </p>\1</li>", thetext)

    return thetext

##################

def liprename(txt):

    the_inside = txt.group(1)

    component.something_changed = True
    current_counter = component.lipcounter
    component.lipcounter += 1

    if "<lip>" in the_inside:  # replace the last <lip> by <lipN>
        the_inside_start, the_inside_end = the_inside.rsplit("<lip>", 1)
        the_inside = the_inside_start + "<lip" + str(current_counter) + ">" + the_inside_end
        return "<lip>" + the_inside + "</lip" + str(current_counter) + ">"
    else:
        return "<lip" + str(current_counter) + ">" + the_inside + "</lip" + str(current_counter) + ">"

##################

def index_fix(txt):

    the_text = txt.group(1)

    if the_text.startswith("<main>"):
        return "<index>" + the_text + "</index>"

    elif "!" not in the_text:
        return "<index><main>" + the_text + "</main></index>"

    elif "<m>" in the_text:   # poor hack to handle factorial
        return "<index><main>" + the_text + "</main></index>"

    else:
        this_entry = the_text.split("!")
        the_answer = "<main>" + this_entry.pop(0) + "</main>"
        for sub in this_entry:
            the_answer += "<sub>" + this_entry.pop(0) + "</sub>"

    return "<index>" + the_answer + "</index>"
  

##################

def pgtombx(text):

    thetext = text

    thetext = myoperations.pgpreprocess(thetext)
# to do:
# HINTs
# multiple solutions: BasicAlgebra/SystemsOfLinearEquations/SystemEquation40.pg

    ERROR_MESSAGE = ""

    # find the defined variables, for later interpreting [________]{$var}
    predefined_variables = re.findall(r"(\$[a-zA-Z0-9_]+\s*=\s*\$[a-zA-Z0-9_]+)\s*->\s*cmp", thetext)
    # print "predefined_variables", predefined_variables
    for varpair in predefined_variables:
        var, evaluator = varpair.split("=")
        var = var.strip()
        evaluator = evaluator.strip()
        component.defined_variables[var] = evaluator
    # need to do the same for PopUp and RadioButtons

    # extract the metadata
    the_metadata, everything_else = thetext.split("\nDOCUMENT();")

    the_metadata = re.sub("#{5,}", "", the_metadata)
    the_metadata = the_metadata.strip()

    the_metadata = utilities.magic_character_convert(the_metadata, "text")

    # extract the macros
    the_macros = re.sub("#{5,}.*", "", everything_else, 0, re.DOTALL)
    everything_else = re.sub(".*?#{5,}", "", everything_else, 1, re.DOTALL)

    the_macros_mbx = myoperations.wwmacros(the_macros)

    if "BEGIN_HINT" in everything_else:
        ERROR_MESSAGE += "ERROR: HINTs not implemented properly\n"
        print "file contains non-PGML HINTs, which are not implemented yet"
    if "BEGIN_TEXT" in everything_else:
        ERROR_MESSAGE += "ERROR: TEXT not implemented properly\n"
        print "file contains non-PGML TEXT, which is not implemented yet"
    if "BEGIN_SOLUTION" in everything_else:
        ERROR_MESSAGE += "ERROR: SOLUTION not implemented properly\n"
        print "file contains non-PGML SOLUTION, which is not implemented yet"

    # find the ANSwer
    re_ANS = "\nANS\((.*?)\);"
    the_answers = re.findall(re_ANS, everything_else, re.DOTALL)
    the_answers = [answer.strip() for answer in the_answers]
    the_answer_variables = [re.search(r"(\$[a-zA-Z0-9_]+)", answer).group(1) for answer in the_answers]
    everything_else = re.sub(re_ANS, "", everything_else, 0, re.DOTALL)
    the_answer_mbx = ""
    for answer in the_answers:
        answer = utilities.magic_character_convert(answer, "code")
        the_answer_mbx += "$ansevaluator = " + answer + "\n"

    # extract the problem statement
    re_statement = "BEGIN_PGML(.*)END_PGML\n"
    try:
        the_statement = re.search(re_statement, everything_else, re.DOTALL).group(1)
        everything_else = re.sub(re_statement, "", everything_else, 0, re.DOTALL)
   #     print "the_statement is", the_statement[:30]
    except AttributeError:
        the_statement = "STATEMENT_NOT_PARSED_CORRECTLY"
        ERROR_MESSAGE += "ERROR: file does not contain a statement\n"
        print "file does not contain a statement"

            # extract the variables in the statement
    vars_in_statement = re.findall(r"(\$[a-zA-Z0-9_]+)", the_statement)
    vars_in_statement = list(set(vars_in_statement))  # remove duplicates
#    print "vars1: ", vars_in_statement

    the_statement_p = the_statement.split("\n\n")
    previous_par = ""
    the_statement_p_mbx = []
    for par in the_statement_p:
     #   print "THIS par", par
        par = par.strip()
        if not par:
            if previous_par == "p":
                the_statement_p_mbx[-1] += "</p>"
            elif previous_par == "li":
                the_statement_p_mbx[-1] += "\n</ul>\n</p>"
            previous_par = ""
            continue
        if par.startswith("* "):
            par = "<li><p>" + par[2:].strip() + "</p></li>"
            if previous_par != "li":
                par = "<p>\n<ul>" + "\n" + par
                previous_par = "li"
        elif previous_par == "p":  # this line is a continuation of the previous paragraph
            pass # do nothing, because we are just processing another ine in the current paragraph
        else: # we must be starting a new paragraph
            par = "<p>" + par
            previous_par = "p"
        par = myoperations.pgmarkup_to_mbx(par, the_answer_variables)
     #   print "par revised", par
        the_statement_p_mbx.append(par)

    the_statement_mbx = "<statement>" + "\n"
    the_statement_mbx += "\n".join(the_statement_p_mbx)
    the_statement_mbx += "\n</statement>" + "\n"



    # extract the solution
    re_solution = "BEGIN_PGML_SOLUTION(.*)END_PGML_SOLUTION"
    try:
        the_solution = re.search(re_solution, everything_else, re.DOTALL).group(1)
        everything_else = re.sub(re_solution, "", everything_else, 0, re.DOTALL)
    except AttributeError:
        the_solution = "SOLUTION_NOT_PARSED_CORRECTLY"
        ERROR_MESSAGE += "ERROR: file does not contain a solution\n"
        print "file does not contain a solution\n"

    the_solution = the_solution.strip()

        # extract the variables in the solution
    vars_in_solution = re.findall(r"(\$[a-zA-Z0-9_]+)", the_solution)
#    print "vars2: ", vars_in_solution
    vars_in_solution = list(set(vars_in_solution))  # remove duplicates
#    print "vars: ", vars_in_solution

    the_solution_mbx = "<solution>" + "\n"
    the_solution_p = the_solution.split("\n\n")
    for par in the_solution_p:
        par = par.strip()
        par = myoperations.pgmarkup_to_mbx(par, the_answer_variables)
        the_solution_mbx += "<p>" + par + "</p>" + "\n"
    the_solution_mbx += "</solution>" + "\n"

    #throw away things that are not needed in the mbx version
    things_to_throw_away = [
           r"TEXT\(beginproblem\(\)\);",
           r"ENDDOCUMENT\(\);",
           r"#{5,}"
           ]
    for junk in things_to_throw_away:
        everything_else = re.sub("\s*" + junk + "\s*", "\n", everything_else)

    # now everything_else contains the pg-code.  In there, we convert
    # < or & to &lt; or &amp;
#    everything_else = re.sub("&", "&amp;", everything_else)
#    everything_else = re.sub("<", "&lt;", everything_else)

    for str in mapping.pg_macro_files:
        if str in everything_else:
            if mapping.pg_macro_files[str] not in component.extra_macros:
                component.extra_macros.append(mapping.pg_macro_files[str])

    everything_else = utilities.magic_character_convert(everything_else, "text")

    the_pgcode_mbx = "<pg-code>" + "\n"
    the_pgcode_mbx += everything_else.strip()
    the_pgcode_mbx += "\n\n" + the_answer_mbx
    the_pgcode_mbx += "\n" + "</pg-code>" + "\n"

    all_vars = list(set(vars_in_statement + vars_in_solution))

    the_setup_mbx = "<setup>" + "\n"
    for var in all_vars:
        the_setup_mbx += '<var name="' + var + '">' + "\n"
        the_setup_mbx += '  <!--<static></static>-->' + "\n"
        the_setup_mbx += '</var>' + "\n"

    the_setup_mbx += the_pgcode_mbx
    the_setup_mbx += "</setup>" + "\n"
#    print the_macros_mbx
#    print the_statement_mbx
#    print the_answer_mbx
#    print the_solution_mbx
#    print the_setup_mbx

#    print "----------------"
#    print everything_else
#    print "----------------"

 #   the_output = ERROR_MESSAGE
    the_output = ""
    the_output += '<?xml version="1.0" encoding="UTF-8" ?>' + "\n"
    the_output += "\n" + "<exercise>" + "\n"
    the_output += "<original-metadata>" + "\n"
    the_output += the_metadata
    the_output += "\n" + "</original-metadata>" + "\n"
    the_output += "\n"
    the_output += '<webwork seed="1">' + "\n"
    the_output += the_macros_mbx
    the_output += "\n"
    the_output += the_setup_mbx
    the_output += "\n"
    the_output += the_statement_mbx
    the_output += "\n"
    the_output += the_solution_mbx
    the_output += "\n" + "</webwork>" + "\n"
    the_output += "</exercise>" + "\n"

    the_output = mbx_pp(the_output)

    return the_output

######################

def mbx_transclude(text):

    thetext = text

    thetext = re.sub(r"<transclude\s*(.*?)\s*/>", mbx_transcl, thetext)

    return thetext

#--------------------#

def mbx_transcl(txt):

    thedata = txt.group(1)

    parameters = ["src", "id-postfix", "id-include", "wrapper"]
    paramval = {}

    for param in parameters:
        try:
            paramval[param] = re.search(param + '=("|\')([^ /]+)("|\')', thedata).group(2)
        except AttributeError:
            paramval[param] = ""

    the_referenced_item = utilities.environment_by_id(paramval["src"], component.onefile)
    the_referenced_item = the_referenced_item.strip()

    if "<transclude " in the_referenced_item:
        the_referenced_item = mbx_transclude(the_referenced_item)

    if paramval["wrapper"] == "no":   # remove starting and ending tags
        the_referenced_item = re.sub("^<[^>]+>", "", the_referenced_item, 1)
        the_referenced_item = re.sub("</[^>]+>$", "", the_referenced_item, 1)
        the_referenced_item = the_referenced_item.strip()
        # and remove the title
        the_referenced_item = re.sub("^<title>.*?</title>\s*", "", the_referenced_item, 1)

    if paramval["id-postfix"]:
        new_postfix = paramval["id-postfix"]
        print "new_postfix", new_postfix
        the_referenced_item = re.sub(r'xml:id=("|\')([^ "\']+)\1', r"xml:id=\1\2" + new_postfix + r"\1", the_referenced_item)

    elif not paramval["id-include"] or paramval["id-include"] == 'no':
        the_referenced_item = re.sub('xml:id=("|\')[^"\']+("|\')\s*', "", the_referenced_item)

    # remove a possible space before > in the starting tag
    the_referenced_item = re.sub("\s*<([a-z_\-]+)\s+>", r"<\1>", the_referenced_item)

    return the_referenced_item

