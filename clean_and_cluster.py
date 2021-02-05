# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Ethan Zaruba-Walker
# Description: Clean and cluster class is a series of methods for analyzing the input of a user faced with an open ended question in the form of a form.
# The question in question is: 'Clubs, athletics, and activities participated in during high school & college'
# This question was taken from the Boulder, Colorado IFC On The Hill Rush records.
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class cleanAndCluster:
    
    def __init__(self, column, act_clusters={}):
        import re
        import numpy as np
        
        try:
            import lumberJack as lj
            self.logging = True
            print('STATUS: Successfully imported lumberJack. Class can be initialized with logger')
        except:
            self.logging = False
            print('STATUS: Failed to load lumberJack.')
            
        self.delimiters = [', ', '\n', ' and ', '. ', '- ']
        self.null_words = ['high', 'school', 'played', "I", 'highschool', "a","about","above","after","again","against","ain","all","am","an","and","any","are","aren","aren't","as","at","be","because","been","before","being",
                            "below","between","both","but","by","can","couldn","couldn't","d","did","didn","didn't","do","does","doesn","doesn't","doing","don","don't","down","during",
                            "each","few","for","from","further","had","hadn","hadn't","has","hasn","hasn't","have","haven","haven't","having","he","her","here","hers","herself","him",
                            "himself","his","how","i","if","in","into","is","isn","isn't","it","it's","its","itself","just","ll","m","ma","me","mightn","mightn't","more","most","mustn",
                            "mustn't","my","myself","needn","needn't","no","nor","not","now","o","of","off","on","once","only","or","other","our","ours","ourselves","out","over","own",
                            "re","s","same","shan","shan't","she","she's","should","should've","shouldn","shouldn't","so","some","such","t","than","that","that'll","the","their","theirs",
                            "them","themselves","then","there","these","they","this","those","through","to","too","under","until","up","ve","very","was","wasn","wasn't","we","were","weren",
                            "weren't","what","when","where","which","while","who","whom","why","will","with","won","won't","wouldn","wouldn't","y","you","you'd","you'll","you're","you've",
                            "your","yours","yourself","yourselves","could","he'd","he'll","he's","here's","how's","i'd","i'll","i'm","i've","let's","ought","she'd","she'll","that's","there's",
                            "they'd","they'll","they're","they've","we'd","we'll","we're","we've","what's","when's","where's","who's","why's","would","able","abst","accordance","according",
                            "accordingly","across","act","actually","added","adj","affected","affecting","affects","afterwards","ah","almost","alone","along","already","also","although","always",
                            "among","amongst","announce","another","anybody","anyhow","anymore","anyone","anything","anyway","anyways","anywhere","apparently","approximately","arent","arise",
                            "around","aside","ask","asking","auth","available","away","awfully","b","back","became","become","becomes","becoming","beforehand","begin","beginning","beginnings",
                            "begins","behind","believe","beside","besides","beyond","biol","brief","briefly","c","ca","came","cannot","can't","cause","causes","certain","certainly","co","com",
                            "come","comes","contain","containing","contains","couldnt","date","different","done","downwards","due","e","ed","edu","effect","eg","eight","eighty","either","else",
                            "elsewhere","end","ending","enough","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","except","f","far","ff","fifth",
                            "first","five","fix","followed","following","follows","former","formerly","forth","found","four","furthermore","g","gave","get","gets","getting","give","given","gives",
                            "giving","go","goes","gone","got","gotten","h","happens","hardly","hed","hence","hereafter","hereby","herein","heres","hereupon","hes","hi","hid","hither","home","howbeit",
                            "however","hundred","id","ie","im","immediate","immediately","importance","important","inc","indeed","index","information","instead","invention","inward","itd","it'll","j",
                            "k","keep","keeps","kept","kg","km","know","known","knows","l","largely","last","lately","later","latter","latterly","least","less","lest","let","lets","like","liked",
                            "likely","line","little","'ll","look","looking","looks","ltd","made","mainly","make","makes","many","may","maybe","mean","means","meantime","meanwhile","merely","mg",
                            "might","million","miss","ml","moreover","mostly","mr","mrs","much","mug","must","n","na","name","namely","nay","nd","near","nearly","necessarily","necessary","need",
                            "needs","neither","never","nevertheless","new","next","nine","ninety","nobody","non","none","nonetheless","noone","normally","nos","noted","nothing","nowhere","obtain",
                            "obtained","obviously","often","oh","ok","okay","old","omitted","one","ones","onto","ord","others","otherwise","outside","overall","owing","p","page","pages","part",
                            "particular","particularly","past","per","perhaps","placed","please","plus","poorly","possible","possibly","potentially","pp","predominantly","present","previously",
                            "primarily","probably","promptly","proud","provides","put","q","que","quickly","quite","qv","r","ran","rather","rd","readily","really","recent","recently","ref",
                            "refs","regarding","regardless","regards","related","relatively","research","respectively","resulted","resulting","results","right","run","said","saw","say","saying",
                            "says","sec","section","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sent","seven","several","shall","shed","shes","show","showed","shown",
                            "showns","shows","significant","significantly","similar","similarly","since","six","slightly","somebody","somehow","someone","somethan","something","sometime","sometimes",
                            "somewhat","somewhere","soon","sorry","specifically","specified","specify","specifying","still","stop","strongly","sub","substantially","successfully","sufficiently","suggest",
                            "sup","sure","take","taken","taking","tell","tends","th","thank","thanks","thanx","thats","that've","thence","thereafter","thereby","thered","therefore","therein","there'll",
                            "thereof","therere","theres","thereto","thereupon","there've","theyd","theyre","think","thou","though","thoughh","thousand","throug","throughout","thru","thus","til","tip",
                            "together","took","toward","towards","tried","tries","truly","try","trying","ts","twice","two","u","un","unfortunately","unless","unlike","unlikely","unto","upon","ups","us",
                            "use","used","useful","usefully","usefulness","uses","using","usually","v","value","various","'ve","via","viz","vol","vols","vs","w","want","wants","wasnt","way","wed",
                            "welcome","went","werent","whatever","what'll","whats","whence","whenever","whereafter","whereas","whereby","wherein","wheres","whereupon","wherever","whether","whim",
                            "whither","whod","whoever","whole","who'll","whomever","whos","whose","widely","willing","wish","within","without","wont","words","world","wouldnt","www","x","yes","yet",
                            "youd","youre","z","zero","a's","ain't","allow","allows","apart","appear","appreciate","appropriate","associated","best","better","c'mon","c's","cant","changes","clearly",
                            "concerning","consequently","consider","considering","corresponding","course","currently","definitely","described","despite","entirely","exactly","example","going","greetings",
                            "hello","help","hopefully","ignored","inasmuch","indicate","indicated","indicates","inner","insofar","it'd","keep","keeps","novel","presumably","reasonably","second","secondly",
                            "sensible","serious","seriously","sure","t's","third","thorough","thoroughly","three","well","wonder"]
    
        
        self.column = column
        self.act_clusters = act_clusters
        return
        
        #self.gen_act_counts(column)
        #self.gen_total_word_counts(column)
        #print(self.total_word_counts)
        
        #self.clean_column(self.column)
        #return self.cleaned_column
    
        
        
    def gen_act_counts(self, arr=[], from_clusters=False):
        if self.logging == True:
            import datetime as dt
            #s = dt.datetime.now().time       
        if from_clusters: # %%%---> Case to generate column_wordcounts from clusters. This is more effective for clustering new responses but requires a pre-existing clusters object
            try: #try to generate counts based on number of sub_acs per ac_parent
                sub_acs_per_parent = []
                ac_totals = []
                for ac in self.act_clusters.keys():
                    sub_acs_per_parent.append(len(self.act_clusters[ac].keys()))
                    ac_totals.append(sum(self.act_clusters[ac].values()))
                act_counts = {'activity': self.act_clusters.keys(), 'counts': ac_totals}
                self.act_counts = act_counts
                self.act_counts_df = pd.DataFrame.from_dict(act_counts).sort_values(['counts'], ascending=False).reset_index().drop('index', axis=1)
                print('Act_counts created from clusters successfully, length is {}'.format(len(act_counts['activity'])))
            except:
                print('Creating counts from clusters failed!')
                
        else:
            try:
                if len(arr) == 0:
                    col = np.array(self.column)
                else:
                    col = np.array(arr)
                new_arr = []
                for item in col:
                    try: 
                        split_item = item.split(', ')
                        for item in split_item:
                            new_arr.append(item.lower())
                    except: pass

                unique, counts = np.unique(new_arr, return_counts=True)
                act_counts = {'activity': unique, 'counts': counts}
                self.act_counts = act_counts
                self.act_counts_df = pd.DataFrame.from_dict(act_counts).sort_values(['counts'], ascending=False).reset_index().drop('index', axis=1)
            except:
                print('Shiiiiiiiiit, Creating counts from column failed!')
            
            #if self.logging == True:
                #te = dt.datetime.now().time - s
                
    def gen_total_word_counts(col):
        # get the column as one long string
        self.total_word_counts = {}
        col_as_string = ''
        item_count = 0
        for item in col:
            col_as_string += str(item)+' ,., '
            item_count += 1

        all_items = re.findall('\w+', col_as_string)
        print('All_items: '+str(len(all_items)))
        
        words, counts = np.unique(all_items, return_counts=True)
        print('Words has {} items'.format(len(words)))

        for i in range(len(words)):
            if words[i] in self.null_words: # True: the word weare looking at has been identified as a Null word so we want to give it a count of 0
                self.total_word_counts[words[i]] = 0
            else: # False: The word we are looking at is not found in the null_words object so we will continue like normal, g
                self.total_word_counts[str(words[i])] = counts[i]
            # print('word: {}\tcount: {}'.format(words[i], counts[i]))
        
        #print(self.total_word_counts)
        #return self.total_word_counts
    
    def fragment_response(response):
        all_fragments = []
        
        for delim in self.delimiters:
            if delim in response:
                split_response = response.split(delim)

                for fragment in split_response:
                    all_fragments.append(fragment)

            else:
                pass
            
        #print('Fragments: '+str(all_fragments))
        return all_fragments
    
    def sterilize_response(response):
        standard_delim = ', '
        pass
        # identify and standardize delimiters
        for delim in self.delimiters:
            if delim in response: # True: the delimiter is in the response, we should replace it with a ", "
                response = response.replace(delim, standard_delim)
            else:
                pass

        # create fragments and fragment counts
        # for each fagment, 
        #   convert to all lowercase list of words without punctuation
        #   generate word count array
        split_response = response.split(standard_delim)
        sterile_response = ''
        fragmented_counts = []
        for frag in split_response:
            frag_words = re.findall('\w+', frag) # fragment words is now a list of words without punctuation
            string_frag = ' '.join(frag_words) # this joins the fragment words around spaces. Result: "i participated in varsity soccer"
            sterile_response += string_frag.lower()+standard_delim # this lowers the fragment_string and adds the standardized delimiter to the end of the string to be rejoined with the rest of the fragements
            # convert to lowercase list of words
            # remove punctuaion
            
            print('Fragment has been cleaned: {}'.format(fragment))
            
            fragmented_counts.append(self.gen_fragment_word_counts(string_frag.lower.split(' ')))
        # return sterile_response = {"i participated in varsity soccer, football, key club": [[0, 4, 8, 64, 41], [68], [4, 78]]}



    def gen_fragment_word_counts(self, words):
        counts = []
        for word in words:
            # counts.append(self.total_word_counts['counts'][int(self.total_word_counts['words'].index(word))]) # this long line adds the count of the word to counts. This can probably be done a better way...
            # print(re.findall('\w+',word))
            try:
                counts.append(self.total_word_counts[word.title()])# try to lookup the word in total_word_counts and if found, add the count to the counts array
            except:
                counts.append(0) # if the word cant be found in total_word_counts, append a "0" to the counts array
        return counts
            
    
    def cluster_fragment(self, fragment, words, counts):
        max_word = re.findall('\w+',words[counts.index(max(counts))])[0] # this just strips everything that isnt alphanumeric from the word with the highest count
        
        if max_word in self.act_clusters: # True: the word with the highest count is found in act_clusters as a parent
            if fragment in self.act_clusters[max_word]: # True, True: the entire fragment is found as a child of max_word
                self.act_clusters[max_word][fragment] += 1
            else: # True, False: the max_word is in act_clusters but fragment is not found as a child. Create it and give it a count of 1
                self.act_clusters[max_word][fragment] = 1
        else: # False, False: max_word is not found in act_clusters. create it and make fragment its child with a count of 1
            self.act_clusters[max_word] = {}
            self.act_clusters[max_word][fragment] = 1
            
        return max_word
    
    def drop_stop_words(self, text):
        without = ''
        words = text.split(' ')
        for word in words:
            if word not in self.null_words:
                without += word+' '
            else:
                pass
        return without.strip()
    
    
    def clean_with_counts(self, resp):
        resp = self.drop_stop_words(resp)
        extracted_acs = set()
        print('Response: {}'.format(resp))
        fragments = self.fragment_response(resp)
        print('Fragments: {}'.format(fragments))
        
        for frag in fragments:
            frag_words = frag.split(' ')
            frag_word_counts = self.gen_fragment_word_counts(frag_words)
            fragment_parent = self.cluster_fragment(frag, frag_words, frag_word_counts)
            print('Fragment parent: {}'.format(fragment_parent))
            extracted_acs.add(fragment_parent)
        
        return extracted_acs
        

        
        
    def refine_clusters(self, act_clusters):
        act_clusters = self.act_clusters
        #for ac_parent in act_clusters:
            # sort the sub_acs by frequency 
            # find some way to determine refined parents to look for
            # only allow the most specific refined parent per sub_ac
            # for each refined_parent, search for occurences in sub_acs and and output a new refined sub_ac dict
            # if a refined_parent is found in the sub_ac, isolate it and add it to the refined sub_acs
                # for the sub ac that is not part of the isolated refined sub_ac, do something with it, either delete it or put it somewhere else
                # add occurances of other ac_parents to their respective cluster 
            
        
    
                
    def clean_column(self, col, with_clusters=False):
        #self.act_counts = gen_act_counts(self.col)
        if with_clusters: # True: clean the column using the clean_with_clusters() method
            cleaned_col = []
            for response in col:
                cleaned_col.append(self.clean_with_clusters(response, self.act_clusters))
            self.cleaned_col = cleaned_col
        else: # Flase: clean the column using the clean_with_counts() method
            cleaned_col = []
            for response in col:
                
                cleaned_col.append(self.clean_with_counts(response))
            #return cleaned_col
            self.cleaned_col = cleaned_col

    def clean_with_clusters(self, resp, clusters):
        extracted_acs = []
        resp = resp.split(' ')
        for ac_parent in clusters.keys():
            try:
                ac_parent_index = resp.index(ac_parent)
                sub_acs = clusters[ac_parent].keys()
                extracted_acs.append(look_for_sub_acs(resp, ac_parent_index, sub_acs))
            except:
                pass
        return extracted_acs
        

    
    
    def look_for_sub_acs(resp, p1_index, sub_acs):
        for sub_ac in sub_acs:
            ac_paent_index = sub_ac.index(resp[p1_index])
            if ac_parent_index == 0:
                #look right
                right = bool(sub_ac[-1] == resp[(len(sub_ac) - ac_parent_index + 1) + p1_index])
                #That line looks for the right most word in the sub ac at it's corresponding index in the response, aligned on the ac_parent
            elif ac_parent_index == (len(sub_ac)-1):
                left = bool(sub_ac[0] ==resp[(p1_index - ac_parent_index)])
                #That line looks for the left most word in the sub ac at the same distance from the ac parent in the resp list, left will be True if they are the same 
            else:
                right = bool(sub_ac[-1] == resp[(len(sub_ac) - ac_parent_index + 1) + p1_index])
                left = bool(sub_ac[0] ==resp[(p1_index - ac_parent_index)])
            if left or right:
                ac_parent = resp[p1_index]
                print('Found {} in response: {}'.format(ac_parent, resp))
                self.clusters[ac_parent][sub_ac] += 1
                return sub_ac
            else:
                pass 
        
    def clean_and_cluster(self, item, act_clusters, act_counts):
        extracted_acs = []
        # present_delims = [list of delimiters present in the response, split on each one of them]
        if ',' in str(item): # they seperated values by comma
            activities = item.split(', ')
            #print('Activities: {}'.format(activities))
            for ac in activities:
                ac = ac.lower()
                try: # to split on the space char
                    ac_words = ac.split(' ')
                    #print('--Activity words: {}'.format(ac_words))

                    #Determine the ac_parent
                    word_counts = []
                    for word in ac_words: 
                        word = word.lower()
                        try:
                            word_c = act_counts['counts'][list(act_counts['activity']).index(word)]
                            #print('-- --Focused word: {}, counts: {}'.format(word, word_c))
                            word_counts.append(word_c)
                        except:
                            #print('-- --Skipped word: {}'.format(word))
                            word_counts.append(0)
                    # =========WORD_COUNTS has been created ===========
                    if (max(word_counts) != 0):
                        for word in ac_words:
                            if word_counts[ac_words.index(word)] > 30: # threshhold required to be declared a parent. Useful for detecting multiple cluster names given in a sentence format.
                                ac_parent = word
                                ac_child = ac
                            else:
                                ac_parent = ac_words[word_counts.index(max(word_counts))]
                                ac_child = ac
                            #print('Activity parent: {}'.format(ac_parent))
                    else: # none of the words in the activity are in act_counts, make the ac the parent and child
                        ac_parent = ac
                        ac_child = ac
                    #========================


                    # if the ac parent is club then we are interested in the sub_ac
                    if ac_parent == 'club':
                        extracted_acs.append(ac_child)
                    else:
                        extracted_acs.append(ac_parent)


                    # ac_parent has been set for the list of words in response, cluster ac_parent and ac_child    
                    if ac_parent in act_clusters.keys():
                        #the parent is defined
                        if ac in act_clusters[ac_parent].keys():
                            #the parent and child are defined
                            act_clusters[ac_parent][ac] += 1
                            #print('-- -- --Count of child: {} incramented'.format(ac))
                        else:
                            #the parent is defined but the child isnt
                            act_clusters[ac_parent][ac] = 1
                            #print('-- -- --Created child: {}'.format(ac))
                    else:
                        #the parent is not defined
                        act_clusters[ac_parent] = {ac: 1}
                        #print('-- -- --Created parent: {} and child: {}'.format(ac_parent, ac))
                    #==========================


                except:
                    extracted_acs.append(ac.lower())
                    ac_parent = ac
                    if ac_parent in act_clusters.keys():
                        #the parent is defined
                        if ac in act_clusters[ac_parent].keys():
                            #the parent and child are defined
                            act_clusters[ac_parent][ac] += 1
                            #print('-- -- --Count of child: {} incramented'.format(ac))
                        else:
                            #the parent is defined but the child isnt
                            act_clusters[ac_parent][ac] = 1
                            #print('-- -- --Created child: {}'.format(ac))
                    else:
                        #the parent is not defined
                        act_clusters[ac_parent] = {ac: 1}
                        #print('-- -- --Created parent: {} and child: {}'.format(ac_parent, ac))

            #print('Activity parent: {}'.format(ac_parent))
        return extracted_acs
    
    def reset_clusters(self):
        self.act_clusters = {'soccer': {}, 'club': {}, 'tennis': {}}
        return
    
    def eval_self(self):
        act_clusters = self.act_clusters
        sub_ac_total = 0
        for ac_key in act_clusters.keys():
            sub_ac_total += sum(act_clusters[ac_key].values())

        cluster_names = act_clusters.keys()
        self.cluster_names = cluster_names
        self.sub_ac_total = sub_ac_total
        
        try: # to calculate retention
            l = list(filter(lambda a: a != 'NaN', self.cleaned_col))
            l = len(list(filter(lambda a: len(a) > 0, l)))
            self.retention = l / len(self.column)
        except:
            pass
        
        sub_ac_spreads = []
        ac_totals = []
        for ac in act_clusters.keys():
            sub_ac_spreads.append(len(act_clusters[ac].keys()))
            ac_totals.append(sum(act_clusters[ac].values()))
        self.avg_cluster_size = np.average(sub_ac_spreads)
        self.avg_ac_total = np.average(ac_totals)
        
        print('Clusters: {} \nSub Activities: {}'.format(len(self.act_clusters.keys()), sub_ac_total))
        try:
            print('Data Retention: {} \nAvg. Cluster Size: {} \nAvg. ac_total: {}'.format(self.retention, self.avg_cluster_size, self.avg_ac_total))
        except: pass
        #return clusters, sub_ac_total 