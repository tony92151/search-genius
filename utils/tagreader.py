
"""
Ctags uses a variety of tag kinds to classify different types of entities in the source code. 
The tag kind, represented by a single character in the tag file, helps to identify what kind of programming construct each tag represents. 
Here are some common tag kinds you might encounter, especially in the context of languages like C, C++, Python, and others:

f: Function or method.
c: Class.
m: Member of a class, such as a field or an attribute.
v: Variable or a constant.
t: Type definition (like typedefs in C or structs).
s: Structure name (common in C and C++).
u: Union name (common in C and C++).
e: Enumerator name, for elements of enumeration types.
g: Enumeration name, for enumeration types themselves.
p: Prototype or forward declaration.
d: Macro or define (common in C-like languages).
l: Local variables (scope-limited variables).
n: Namespace.
x: External and forward variable declarations (in some languages).
i: Import statements (common in languages like Python and Java).


For example:
extract_email_b	app/c.py	/^from b import extract_email as extract_email_b$/;"	Y	nameref:unknown:extract_email
|---Tag Name--|-File Name-|---------------------Ex-command--------------------|-Tag Kind-|---Extension Fields-------|

The line you're referring to is an entry from a Ctags-generated tag file. Let's break it down:

* Tag Name (extract_email_b): This is the name of the tag, which, in this case, is extract_email_b. It's the name used in the code for a particular element, which Ctags has identified and indexed.
* File Name (c.py): This specifies the file in which the tag is located. Here, c.py is the file containing the reference to extract_email_b.
* Ex-command (/^from b import extract_email as extract_email_b$/): This part is an Ex command (from the ex/vim text editors) that, when executed, would position the cursor at the line where the tag is defined. Here, it's pointing to the line where extract_email_b is imported from module b.
* Tag Kind (;"): This separator (;) followed by a quote (") is a field delimiter that separates the Ex command from the tag kind and other extension fields.
* Tag Kind Identifier (Y): The Y represents the kind of tag. In many Ctags formats, Y indicates a reference to a symbol, which is not the definition itself but a usage or a call to that symbol.
* Extension Fields (nameref:unknown:extract_email):
    - nameref: This indicates that the tag is a reference to another symbol. In this case, extract_email_b is a reference to some other entity.
    - unknown: This often means that Ctags could not fully resolve the reference. It knows extract_email_b is a reference to extract_email, but it might not be able to determine exactly which extract_email it refers to, especially if there are multiple definitions (like in your case with a.py and b.py).
    - extract_email: This is the original name of the symbol that extract_email_b refers to. It tells you that extract_email_b is essentially extract_email imported from b.py.

"""

def read_tags_file(file_path: str, accept_file: list[str] = [], ignore_keyword_str: list[str] = ["cache"]) -> list[dict]:
    with open(file_path, 'r', errors='ignore') as file:
        lines = file.readlines()

    tags = []
    for line in lines:
        if line.startswith('!'):  # Skip metadata lines
            continue
        line = line[:-1] if line.endswith('\n') else line
        parts = line.split('\t')

        if len(parts) < 5:
            continue

        # if parts[1] not endwith accept_file, continue
        if accept_file and not any(parts[1].endswith(accept) for accept in accept_file):
            continue
        
        # if parts[1] mathch ignore_keyword_str, continue
        if ignore_keyword_str and any(ignore in parts[1] for ignore in ignore_keyword_str):
            continue

        tags.append(
            dict(
                tag_name=parts[0], 
                file_name=parts[1], 
                ex_command=remove_tag_kind(parts[2]),
                tag_kind=parts[3],
                extension_fields=parts[4]
            )
        )
    return tags

def remove_tag_kind(ex_command: str) -> str:
    # alse remove delimiters
    if not ex_command:
        return ex_command
    ex_command = ex_command.split(';"')[0]

    if ex_command.startswith('/') and ex_command.endswith('/'):
        return ex_command[1:-1]