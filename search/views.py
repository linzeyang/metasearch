# Create your views here.
from operator import attrgetter

from django.shortcuts import render_to_response

from bingapi.views import getItemList as bingGetItemList
from blekkoapi.views import getItemList as blekkoGetItemList
from entwebapi.views import getItemList as entwebGetItemList
from texthandle.views import stringProcess, makeCluster

def search(request):
    """
    Central function for request processing and response generation.
    Return HTTP Response object
    """
    raw_query = request.GET.get('query', '')
    
    showBing = request.GET.has_key('bing')
    showBlekko = request.GET.has_key('blekko')
    showEntweb = request.GET.has_key('entweb')
    aggr = request.GET.get('aggr', '')
    cluster = request.GET.get('cluster', '')
    
    errors = validate(raw_query, showBing, showBlekko, showEntweb, aggr)
    
    if errors:
        return render_to_response('start.html', {'errors' : errors})
    
    queries = stringProcess(raw_query)
    
    page = int(request.GET.get('page', '1'))
    
    if 1 <= page <= 6:
        page_list = range(1, 11) # 1, 2, ..., 10
    elif page > 6:
        page_list = range(page - 5, page + 5)
        
    full_path = request.get_full_path()
    
    if aggr == 'false' or aggr == '':
        lists = nonAggrSearch(queries, showBing, showBlekko, showEntweb, page)
        
        if cluster == 'true':
            bingClusters = makeCluster(lists[0])
            blekkoClusters = makeCluster(lists[1])
            entwebClusters = makeCluster(lists[2])
            
            return render_to_response('results_nonaggr.html', 
                {
                    'raw_query' : raw_query,
                    'showBing' : showBing,
                    'showBlekko' : showBlekko,
                    'showEntweb' : showEntweb,
                    'cluster' : True,
                    'bingClusters' : bingClusters,
                    'blekkoClusters' : blekkoClusters, 
                    'entwebClusters' : entwebClusters,
                    'full_path' : full_path,
                    'page_list' : page_list,
                    'current_page': page
                }
            )
        
        elif cluster == 'false' or cluster == '':
            return render_to_response('results_nonaggr.html', 
                {
                    'raw_query' : raw_query,
                    'showBing' : showBing,
                    'showBlekko' : showBlekko,
                    'showEntweb' : showEntweb,
                    'cluster' : False,
                    'bingList' : lists[0],
                    'blekkoList' : lists[1], 
                    'entwebList' : lists[2],
                    'full_path' : full_path,
                    'page_list' : page_list,
                    'current_page': page
                }
            )
    elif aggr == 'true':
        result_list = aggrSearch(queries, showBing, showBlekko, showEntweb, page)
        
        if cluster == 'true':
            clusters = makeCluster(result_list)
            return render_to_response('results_aggr.html', 
                {
                    'raw_query' : raw_query,
                    'showBing' : showBing,
                    'showBlekko' : showBlekko,
                    'showEntweb' : showEntweb,
                    'cluster' : True,
                    'clusters': clusters,
                    'full_path' : full_path,
                    'page_list' : page_list,
                    'current_page': page
                }
            )
            
        elif cluster == 'false' or cluster == '':
            return render_to_response('results_aggr.html', 
                {
                    'raw_query' : raw_query,
                    'showBing' : showBing,
                    'showBlekko' : showBlekko,
                    'showEntweb' : showEntweb,
                    'cluster' : False,
                    'result_list': result_list,
                    'full_path' : full_path,
                    'page_list' : page_list,
                    'current_page': page
                }
            )
        
##################################################################################

def validate(raw_query, showBing, showBlekko, showEntweb, aggr):
    """
    Validate the parameters of HTTP Request on server side.
    Return a list of error strings.
    """
    errors = []

    if raw_query == '':
        errors.append('ERROR: Query cannot be empty!')
    elif len(raw_query) > 100:
        errors.append('ERROR: A query cannot be longer than 100 characters!')
    
    if not (showBing or showBlekko or showEntweb):
        errors.append('ERROR: Choose at least one search engine!')
    elif aggr == 'true' and ((not showBing and not showBlekko) or (not showBlekko and not showEntweb) or (not showBing and not showEntweb)):
        errors.append('ERROR: Choose at lease two search engines for aggregated results!')
    
    return errors
    
##################################################################################

def nonAggrSearch(queries, showBing, showBlekko, showEntweb, page):
    """
    Generate results in non-aggregated mode.
    Returns a list of three result lists
    """
    if showBing:
        bingList = bingGetItemList(queries[0], page, 10)
    else:
        bingList = []
    
    if showBlekko:
        blekkoList = blekkoGetItemList(queries[1], page, 10)
    else:
        blekkoList = []
    
    if showEntweb:
        entwebList = entwebGetItemList(queries[2], page, 10)
    else:
        entwebList = []
        
    return [bingList, blekkoList, entwebList]
    
##################################################################################

def aggrSearch(queries, showBing, showBlekko, showEntweb, page):
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

            if showBing:
                bingList = bingGetItemList(queries[0], engine_page, 50)
            else:
                bingList = []
            if showBlekko:
                blekkoList = blekkoGetItemList(queries[1], engine_page, 50)
            else:
                blekkoList = []
            if showEntweb:
                entwebList = entwebGetItemList(queries[2], engine_page, 50)
            else:
                entwebList = []
            ##################################
            if aggr_page == 0:
                for i in bingList:
                    i.base_score[0] = 100.0 - bingList.index(i)
                for j in blekkoList:
                    j.base_score[1] = 100.0 - blekkoList.index(j)
                for k in entwebList:
                    k.base_score[2] = 100.0 - entwebList.index(k)
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

                
                for i in bingList:
                    i.base_score[0] = offset + 50.0 - bingList.index(i)
                for j in blekkoList:
                    j.base_score[1] = offset + 50.0 - blekkoList.index(j)
                for k in entwebList:
                    k.base_score[2] = offset + 50.0 - entwebList.index(k)
                
                for i in scored_list:
                    if 'BING' in i.source:
                        i.base_score[0] += offset
                    else:
                        for j in bingList:
                            if i.url.lower() == j.url.lower():
                                i.base_score[0] = j.base_score[0]
                                i.source.append('BING')
                                bingList.pop(bingList.index(j))
                                break
                    if 'Blekko' in i.source:
                        i.base_score[1] += offset
                    else:
                        for k in blekkoList:
                            if i.url.lower() == k.url.lower():
                                i.base_score[1] = k.base_score[0]
                                i.source.append('Blekko')
                                blekkoList.pop(blekkoList.index(k))
                                break
                    if 'EntireWeb' in i.source:
                        i.base_score[2] += offset
                    else:
                        for l in entwebList:
                            if i.url.lower() == l.url.lower():
                                i.base_score[2] = l.base_score[0]
                                i.source.append('EntireWeb')
                                entwebList.pop(entwebList.index(l))
                                break
                    i.weighted_score = (i.base_score[0] * bingWeight + i.base_score[1] * blekkoWeight + i.base_score[2] * entwebWeight) * (3 - i.base_score.count(0.0))
            
            ##################################
            while bingList:
                for i in blekkoList:
                    if i.url.lower() == bingList[0].url.lower():
                        bingList[0].base_score[1] = i.base_score[1]
                        bingList[0].source += i.source
                        blekkoList.pop(blekkoList.index(i))
                        break
                for j in entwebList:
                    if j.url.lower() == bingList[0].url.lower():
                        bingList[0].base_score[2] += j.base_score[2]
                        bingList[0].source += j.source
                        entwebList.pop(entwebList.index(j))
                        break
                bingList[0].weighted_score = (bingList[0].base_score[0] * bingWeight + bingList[0].base_score[1] * blekkoWeight + bingList[0].base_score[2] * entwebWeight) * (3 - bingList[0].base_score.count(0.0))
                scored_list.append(bingList.pop(0))
            ##################################
            while blekkoList:
                for i in entwebList:
                    if i.url.lower() == blekkoList[0].url.lower():
                        blekkoList[0].base_score[2] += i.base_score[2]
                        blekkoList[0].source += i.source
                        entwebList.pop(entwebList.index(i))
                        break
                blekkoList[0].weighted_score = (blekkoList[0].base_score[1] * blekkoWeight + blekkoList[0].base_score[2] * entwebWeight) * (3 - blekkoList[0].base_score.count(0.0))
                scored_list.append(blekkoList.pop(0))
            ##################################
            while entwebList:
                entwebList[0].weighted_score = entwebList[0].base_score[2] * entwebWeight
                scored_list.append(entwebList.pop(0))
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

