# function to get all fixed expressions in a sentence in the form of lemma/word sequences and accompanying frequency counts
def get_fixed_expressions(sent, field_to_check):
    # first identify all tokens that have "fixed" dependents
    all_fixed = set()
    for tok in sent:
        if get_basic_deprel(tok["deprel"]) == "fixed":
            all_fixed.add(tok["head"])

    # next, for every "fixed" head, identify the full expression
    fixed_expressions = list()
    for fixed_head in all_fixed:
        curr_expression = sent[fixed_head - 1][field_to_check]
        for tok in sent:
            if get_basic_deprel(tok["deprel"]) == "fixed" and tok["head"] == fixed_head:
                curr_expression += " " + tok[field_to_check]

        fixed_expressions.append(curr_expression)

    return fixed_expressions


# helper function to get basic deprels without subtypes
def get_basic_deprel(deprel):
    return deprel.split(":")[0]


# function to get maximum tree depth in a sentence, where the permitted relations define which relations can be 
# considered in the process
def get_max_tree_depth(sent, permitted_relations=None):
    def is_allowed(deprel_in_question, allowed_list):
        return allowed_list is None or deprel_in_question in allowed_list

    depths = list()
    for tok in sent:
        curr_depth = 0
        new_head = tok["head"]
        deprel_to_check = get_basic_deprel(tok["deprel"]) 
        while is_allowed(deprel_to_check, permitted_relations) and deprel_to_check != "root":
            curr_depth += 1 
            deprel_to_check = get_basic_deprel(sent[new_head - 1]["deprel"])
            new_head = sent[new_head - 1]["head"]

        depths.append(curr_depth)

    return max(depths)

# function to get the root-level deprel of the constituent to which the token in question belongs
def get_root_level_deprel(sent, tok_id):
    if get_basic_deprel(sent[tok_id - 1]["deprel"]) == "root":
        return "root"
    
    curr_id = tok_id
    curr_deprel = get_basic_deprel(sent[curr_id - 1]["deprel"])
    head_id = sent[curr_id - 1]["head"]
    head_deprel = get_basic_deprel(sent[head_id - 1]["deprel"])
    while head_deprel != "root":
        curr_id = head_id
        curr_deprel = get_basic_deprel(sent[curr_id - 1]["deprel"])
        head_id = sent[curr_id - 1]["head"]
        head_deprel = get_basic_deprel(sent[head_id - 1]["deprel"])

    return curr_deprel


# function that returns True if token A dominates token B (i.e. if A is above B in the tree and one can trace a path from B to A 
# only by moving up the tree and never moving down)
def dominates(sent, token_a_id, token_b_id):
    path = list()
    curr_tok_id = token_b_id
    path.append(curr_tok_id)
    while curr_tok_id != 0:
        curr_tok_id = sent[curr_tok_id - 1]["head"]
        path.append(curr_tok_id)
        if token_a_id in path:
            return True

    return False


# function that returns True if the dependency leading to a token is projective (i.e. there is no other relation in the sentence that crosses it)
# adapted from the formal definition in (Nivre, 2006 - Constraints on Non-Projective Dependency Parsing - https://aclanthology.org/anthology-files/anthology-files/pdf/Z/E06/E06-1010.pdf)
def is_projective(sent, tok_id):
    head_id = sent[tok_id - 1]["head"]
    dependent_id = tok_id

    if head_id < dependent_id:
        for k in range(head_id + 1, dependent_id):
            if not dominates(sent, head_id, k):
                return False
    else:
        for k in range(dependent_id + 1, head_id):
            if not dominates(sent, head_id, k):
                return False

    return True


# function that returns the string representation of the whole subtree headed by a token
def get_token_subtree(sent, tok_id, field_to_check="lemma"):
    subtree = ""

    for tok in sent:
        if dominates(sent, tok_id, tok["id"]):
            subtree += tok[field_to_check] + " "

    return subtree.strip(" ")
