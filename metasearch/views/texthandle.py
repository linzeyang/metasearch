# Create your views here.
import urllib

stopword_list = ['a', 'about', 'above', 'across', 'after', 'again', 'against',\
                 'all', 'almost', 'alone', 'along', 'already', 'also',\
                 'although', 'always', 'among', 'an', 'and', 'another',\
                 'any', 'anybody', 'anyone', 'anything', 'anywhere', 'are',\
                 'area', 'areas', 'around', 'as', 'ask', 'asked', 'asking',\
                 'asks', 'at', 'away', 'b', 'back', 'backed', 'backing',\
                 'backs', 'be', 'became', 'because', 'become', 'becomes',\
                 'been', 'before', 'began', 'behind', 'being', 'beings',\
                 'best', 'better', 'between', 'big', 'both', 'but', 'by',\
                 'c', 'came', 'can', 'cannot', 'case', 'cases', 'certain',\
                 'certainly', 'clear', 'clearly', 'come', 'could', 'd', 'did',\
                 'differ', 'different', 'differently', 'do', 'does', 'done',\
                 'down', 'down', 'downed', 'downing', 'downs', 'during', 'e',\
                 'each', 'early', 'either', 'end', 'ended', 'ending', 'ends',\
                 'enough', 'even', 'evenly', 'ever', 'every', 'everybody',\
                 'everyone', 'everything', 'everywhere', 'f', 'face', 'faces',\
                 'fact', 'facts', 'far', 'felt', 'few', 'find', 'finds',\
                 'first', 'for', 'four', 'from', 'full', 'fully', 'further',\
                 'furthered', 'furthering', 'furthers', 'g', 'gave', 'general',\
                 'generally', 'get', 'gets', 'give', 'given', 'gives', 'go',\
                 'going', 'good', 'goods', 'got', 'great', 'greater', 'greatest',\
                 'group', 'grouped', 'grouping', 'groups', 'h', 'had', 'has',\
                 'have', 'having', 'he', 'her', 'here', 'herself', 'high', 'high',\
                 'high', 'higher', 'highest', 'him', 'himself', 'his', 'how',\
                 'however', 'i', 'if', 'important', 'in', 'interest',\
                 'interested', 'interesting', 'interests', 'into', 'is', 'it',\
                 'its', 'itself', 'j', 'just', 'k', 'keep', 'keeps', 'kind',\
                 'knew', 'know', 'known', 'knows', 'l', 'large', 'largely',\
                 'last', 'later', 'latest', 'least', 'less', 'let', 'lets',\
                 'like', 'likely', 'long', 'longer', 'longest', 'm', 'made',\
                 'make', 'making', 'man', 'many', 'may', 'me', 'member',\
                 'members', 'men', 'might', 'more', 'most', 'mostly', 'mr',\
                 'mrs', 'much', 'must', 'my', 'myself', 'n', 'necessary',\
                 'need', 'needed', 'needing', 'needs', 'never', 'new', 'new',\
                 'newer', 'newest', 'next', 'no', 'nobody', 'non', 'noone',\
                 'not', 'nothing', 'now', 'nowhere', 'number', 'numbers', 'o',\
                 'of', 'off', 'often', 'old', 'older', 'oldest', 'on', 'once',\
                 'one', 'only', 'open', 'opened', 'opening', 'opens', 'or',\
                 'order', 'ordered', 'ordering', 'orders', 'other', 'others',\
                 'our', 'out', 'over', 'p', 'part', 'parted', 'parting',\
                 'parts', 'per', 'perhaps', 'place', 'places', 'point',\
                 'pointed', 'pointing', 'points', 'possible', 'present',\
                 'presented', 'presenting', 'presents', 'problem', 'problems',\
                 'put', 'puts', 'q', 'quite', 'r', 'rather', 'really', 'right',\
                 'right', 'room', 'rooms', 's', 'said', 'same', 'saw', 'say',\
                 'says', 'second', 'seconds', 'see', 'seem', 'seemed', 'seeming',\
                 'seems', 'sees', 'several', 'shall', 'she', 'should', 'show',\
                 'showed', 'showing', 'shows', 'side', 'sides', 'since', 'small',\
                 'smaller', 'smallest', 'so', 'some', 'somebody', 'someone',\
                 'something', 'somewhere', 'state', 'states', 'still', 'still',\
                 'such', 'sure', 't', 'take', 'taken', 'than', 'that', 'the',\
                 'their', 'them', 'then', 'there', 'therefore', 'these', 'they',\
                 'thing', 'things', 'think', 'thinks', 'this', 'those', 'though',\
                 'thought', 'thoughts', 'three', 'through', 'thus', 'to', 'today',\
                 'together', 'too', 'took', 'toward', 'turn', 'turned', 'turning',\
                 'turns', 'two', 'u', 'under', 'until', 'up', 'upon', 'us', 'use',\
                 'used', 'uses', 'v', 'very', 'w', 'want', 'wanted', 'wanting',\
                 'wants', 'was', 'way', 'ways', 'we', 'well', 'wells', 'went',\
                 'were', 'what', 'when', 'where', 'whether', 'which', 'while',\
                 'who', 'whole', 'whose', 'why', 'will', 'with', 'within',\
                 'without', 'work', 'worked', 'working', 'works', 'would', 'x',\
                 'y', 'year', 'years', 'yet', 'you', 'young', 'younger',\
                 'youngest', 'your', 'yours', 'z']

punctuations = '~`!@#$%^&*_+={}[]|:;"\',\.<>/?'


def string_process(raw_string):
    """
    Normalize the query with support for Boolean operators.
    Return queries suitable for each search engine.
    """
    raw_tokens = raw_string.split()
    bing_tokens = []
    blekko_tokens = []
    entweb_tokens = []
    add_not = False

    for token in raw_tokens:
        if token == 'AND':
            pass
        elif token == 'OR':
            bing_tokens.append('OR')
            blekko_tokens.append('|')
            entweb_tokens.append('or')
        elif token == 'NOT':
            add_not = True
        else:
            token = token.strip(punctuations).lower()
            if add_not:
                token = '-' + token
                add_not = False
            bing_tokens.append(token)
            blekko_tokens.append(token)
            entweb_tokens.append(token)

    return [urllib.quote(' '.join(bing_tokens)),
            urllib.quote(' '.join(blekko_tokens)),
            urllib.quote(' '.join(entweb_tokens))]


def snippet_process(snippet):
    """
    Split a snippet into a list of tokens, excluding stopwords.
    """
    raw_tokens = snippet.split()
    tokens = []

    for token in raw_tokens:
        token = token.strip(punctuations).lower()

        if not ((token in tokens) or (token in stopword_list) or (token == '')):
            tokens.append(token)

    return tokens


def flatten(lis):
    """
    Flattens a list.
    Return the flattened list.
    """
    if not isinstance(lis, list):
        return [lis]

    if lis == []:
        return lis

    return flatten(lis[0]) + flatten(lis[1:])


def make_cluster(result_list):
    """
    Resemble a list of result items into several clusters.
    Return a list of clusters.
    """
    if result_list == []:
        return []

    num_cluster = 3
    tokens_list = []
    clusters = []

    for i in result_list:
        tokens_list.append(snippet_process(i.snippet))

    while len(clusters) < num_cluster - 1:
        init_lenth = len(clusters)
        flat_tokens = flatten(tokens_list)
        token_dict = {}

        for token in flat_tokens:
            if token in token_dict:
                token_dict[token] += 1
            else:
                token_dict[token] = 1

        sorted_tokens = sorted(token_dict.items(), key=lambda t: t[1],
                               reverse=True)

        for token in sorted_tokens:
            if 0.3 * len(result_list) <= token[1] <= 0.7 * len(result_list):
                single_cluster = []
                rest_results = []
                rest_tokens_list = []

                for tokens in tokens_list:
                    if token[0] in tokens:
                        single_cluster.append(
                            result_list[tokens_list.index(tokens)]
                        )
                    else:
                        rest_results.append(
                            result_list[tokens_list.index(tokens)]
                        )
                        rest_tokens_list.append(tokens)

                clusters.append(single_cluster)
                result_list = rest_results
                tokens_list = rest_tokens_list
                break

        if len(clusters) == init_lenth:
            clusters.append(result_list)
            break

    clusters.append(result_list)

    return clusters
