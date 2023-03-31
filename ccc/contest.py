BEATS = {
    "R": "S",
    "S": "P",
    "P": "R",
}


def solve(data):
    result = []
    for style in data["styles"]:
        a, b = style
        if a == b:
            result.append(a)
        elif BEATS[a] == b:
            result.append(a)
        elif BEATS[b] == a:
            result.append(b)

    return "\n".join(result)
