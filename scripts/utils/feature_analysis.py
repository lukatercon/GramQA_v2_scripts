def has_feature_starting_with(token, pattern):
    if not token.get("feats"):
        return False

    for k in token["feats"].keys():
        if k.startswith(pattern):
            return True

    return False


# gets "Feature=Value" pairs for features starting with the pattern
def get_features_starting_with(token, pattern):
    result = list()

    for k, v in token["feats"].items():
        if k.startswith(pattern):
            result.append(f"{k}={v}")

    return result
