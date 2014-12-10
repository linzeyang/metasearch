# Create your views here.
from operator import attrgetter

from django.shortcuts import render

from metasearch.views.bingapi import get_item_list as bing_get_item_list
from metasearch.views.blekkoapi import get_item_list as blekko_get_item_list
from metasearch.views.entwebapi import get_item_list as entweb_get_item_list
from metasearch.views.texthandle import string_process, make_cluster


def search(request):
    """
    Central function for request processing and response generation.
    Return HTTP Response object
    """
    raw_query = request.GET.get('query', '')
    
    show_bing = 'bing' in request.GET
    show_blekko = 'blekko' in request.GET
    show_entweb = 'entweb' in request.GET
    aggr = request.GET.get('aggr', '')
    cluster = request.GET.get('cluster', '')
    
    errors = validate(raw_query, show_bing, show_blekko, show_entweb, aggr)
    
    if errors:
        return render(request, 'metasearch/start.html', {'errors' : errors})
    
    queries = string_process(raw_query)
    
    page = int(request.GET.get('page', '1'))
    
    if 1 <= page <= 6:
        page_list = range(1, 11) # 1, 2, ..., 10
    elif page > 6:
        page_list = range(page - 5, page + 5)
        
    full_path = request.get_full_path()
    
    if aggr == 'false' or aggr == '':
        lists = non_aggr_search(queries, show_bing, show_blekko, show_entweb, page)
        
        if cluster == 'true':
            bing_clusters = make_cluster(lists[0])
            blekko_clusters = make_cluster(lists[1])
            entweb_clusters = make_cluster(lists[2])
            
            return render(request, 'metasearch/results_nonaggr.html', 
                    {
                        'raw_query' : raw_query,
                        'show_bing' : show_bing,
                        'show_blekko' : show_blekko,
                        'show_entweb' : show_entweb,
                        'cluster' : True,
                        'bing_clusters' : bing_clusters,
                        'blekko_clusters' : blekko_clusters, 
                        'entweb_clusters' : entweb_clusters,
                        'full_path' : full_path,
                        'page_list' : page_list,
                        'current_page': page
                    }
                    )
        
        elif cluster == 'false' or cluster == '':
            return render(request, 'metasearch/results_nonaggr.html', 
                    {
                        'raw_query' : raw_query,
                        'show_bing' : show_bing,
                        'show_blekko' : show_blekko,
                        'show_entweb' : show_entweb,
                        'cluster' : False,
                        'bing_list' : lists[0],
                        'blekko_list' : lists[1], 
                        'entweb_list' : lists[2],
                        'full_path' : full_path,
                        'page_list' : page_list,
                        'current_page': page
                    }
                    )
    elif aggr == 'true':
        result_list = aggr_search(queries, show_bing, show_blekko, show_entweb, page)
        
        if cluster == 'true':
            clusters = make_cluster(result_list)

            return render(request, 'metasearch/results_aggr.html', 
                    {
                        'raw_query' : raw_query,
                        'show_bing' : show_bing,
                        'show_blekko' : show_blekko,
                        'show_entweb' : show_entweb,
                        'cluster' : True,
                        'clusters': clusters,
                        'full_path' : full_path,
                        'page_list' : page_list,
                        'current_page': page
                    }
                    )
            
        elif cluster == 'false' or cluster == '':
            return render(request, 'metasearch/results_aggr.html', 
                    {
                        'raw_query' : raw_query,
                        'show_bing' : show_bing,
                        'show_blekko' : show_blekko,
                        'show_entweb' : show_entweb,
                        'cluster' : False,
                        'result_list': result_list,
                        'full_path' : full_path,
                        'page_list' : page_list,
                        'current_page': page
                    }
                    )
        

def validate(raw_query, show_bing, show_blekko, show_entweb, aggr):
    """
    Validate the parameters of HTTP Request on server side.
    Return a list of error strings.
    """
    errors = []

    if raw_query == '':
        errors.append('ERROR: Query cannot be empty!')
    elif len(raw_query) > 100:
        errors.append('ERROR: A query cannot be longer than 100 characters!')
    
    if not (show_bing or show_blekko or show_entweb):
        errors.append('ERROR: Choose at least one search engine!')
    elif aggr == 'true' and ((not show_bing and not show_blekko) or (not show_blekko and not show_entweb) or (not show_bing and not show_entweb)):
        errors.append('ERROR: Choose at lease two search engines for aggregated results!')
    
    return errors
    

def non_aggr_search(queries, show_bing, show_blekko, show_entweb, page):
    """
    Generate results in non-aggregated mode.
    Returns a list of three result lists
    """
    if show_bing:
        bing_list = bing_get_item_list(queries[0], page, 10)
    else:
        bing_list = []
    
    if show_blekko:
        blekko_list = blekko_get_item_list(queries[1], page, 10)
    else:
        blekko_list = []
    
    if show_entweb:
        entweb_list = entweb_get_item_list(queries[2], page, 10)
    else:
        entweb_list = []
        
    return [bing_list, blekko_list, entweb_list]
    

def aggr_search(queries, show_bing, show_blekko, show_entweb, page):
    """
    Generate results in aggregated mode.
    Return a list of aggregated results.
    """
    bingWeight = 1.737
    blekkoWeight = 1.412
    entwebWeight = 1.0
    
    scored_list = []
    
    aggr_page = 0
    engine_page = 0

    ##########################################
    while aggr_page < page:
        if len(scored_list) < 100:
            engine_page += 1

            if show_bing:
                bing_list = bing_get_item_list(queries[0], engine_page, 50)
            else:
                bing_list = []

            if show_blekko:
                blekko_list = blekko_get_item_list(queries[1], engine_page, 50)
            else:
                blekko_list = []

            if show_entweb:
                entweb_list = entweb_get_item_list(queries[2], engine_page, 50)
            else:
                entweb_list = []
            ##################################
            if aggr_page == 0:
                for i in bing_list:
                    i.base_score[0] = 100.0 - bing_list.index(i)

                for j in blekko_list:
                    j.base_score[1] = 100.0 - blekko_list.index(j)

                for k in entweb_list:
                    k.base_score[2] = 100.0 - entweb_list.index(k)
            ##################################
            else:
                bing_top_score = 0
                blekko_top_score = 0
                entweb_top_score = 0
                
                for i in scored_list:
                    if 'BING' in i.source:
                        if i.base_score[0] > bing_top_score:
                            bing_top_score = i.base_score[0]

                    if 'Blekko' in i.source:
                        if i.base_score[1] > blekko_top_score:
                            blekko_top_score = i.base_score[1]

                    if 'EntireWeb' in i.source:
                        if i.base_score[2] > entweb_top_score:
                            entweb_top_score = i.base_score[2]

                max_top_score = max(bing_top_score, blekko_top_score, entweb_top_score)
                offset = 100.0 - max_top_score

                
                for i in bing_list:
                    i.base_score[0] = offset + 50.0 - bing_list.index(i)

                for j in blekko_list:
                    j.base_score[1] = offset + 50.0 - blekko_list.index(j)

                for k in entweb_list:
                    k.base_score[2] = offset + 50.0 - entweb_list.index(k)
                
                for i in scored_list:
                    if 'BING' in i.source:
                        i.base_score[0] += offset
                    else:
                        for j in bing_list:
                            if i.url.lower() == j.url.lower():
                                i.base_score[0] = j.base_score[0]
                                i.source.append('BING')
                                bing_list.pop(bing_list.index(j))
                                break

                    if 'Blekko' in i.source:
                        i.base_score[1] += offset
                    else:
                        for k in blekko_list:
                            if i.url.lower() == k.url.lower():
                                i.base_score[1] = k.base_score[0]
                                i.source.append('Blekko')
                                blekko_list.pop(blekko_list.index(k))
                                break

                    if 'EntireWeb' in i.source:
                        i.base_score[2] += offset
                    else:
                        for l in entweb_list:
                            if i.url.lower() == l.url.lower():
                                i.base_score[2] = l.base_score[0]
                                i.source.append('EntireWeb')
                                entweb_list.pop(entweb_list.index(l))
                                break

                    i.weighted_score = (i.base_score[0] * bingWeight + i.base_score[1] * blekkoWeight + i.base_score[2] * entwebWeight) * (3 - i.base_score.count(0.0))
            
            ##################################
            while bing_list:
                for i in blekko_list:
                    if i.url.lower() == bing_list[0].url.lower():
                        bing_list[0].base_score[1] = i.base_score[1]
                        bing_list[0].source += i.source
                        blekko_list.pop(blekko_list.index(i))
                        break

                for j in entweb_list:
                    if j.url.lower() == bing_list[0].url.lower():
                        bing_list[0].base_score[2] += j.base_score[2]
                        bing_list[0].source += j.source
                        entweb_list.pop(entweb_list.index(j))
                        break

                bing_list[0].weighted_score = (bing_list[0].base_score[0] * bingWeight + bing_list[0].base_score[1] * blekkoWeight + bing_list[0].base_score[2] * entwebWeight) * (3 - bing_list[0].base_score.count(0.0))
                scored_list.append(bing_list.pop(0))
            ##################################
            while blekko_list:
                for i in entweb_list:
                    if i.url.lower() == blekko_list[0].url.lower():
                        blekko_list[0].base_score[2] += i.base_score[2]
                        blekko_list[0].source += i.source
                        entweb_list.pop(entweb_list.index(i))
                        break
                        
                blekko_list[0].weighted_score = (blekko_list[0].base_score[1] * blekkoWeight + blekko_list[0].base_score[2] * entwebWeight) * (3 - blekko_list[0].base_score.count(0.0))
                scored_list.append(blekko_list.pop(0))
            ##################################
            while entweb_list:
                entweb_list[0].weighted_score = entweb_list[0].base_score[2] * entwebWeight
                scored_list.append(entweb_list.pop(0))
            ##################################
            sorted_list = sorted(scored_list, key = attrgetter('weighted_score'), reverse = True)
            
            result_list = sorted_list[0:50]
            scored_list = sorted_list[50:]
            
            aggr_page += 1
        ##################################
        else:
            result_list = sorted_list[0:50]
            scored_list = sorted_list[50:]
    
            aggr_page += 1
    
    ##########################################
    return result_list

