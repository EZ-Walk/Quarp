# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Ethan Zaruba-Walker
# Version: 1.0.0
# Description: Clean and cluster class is a series of methods for analyzing the input of a user faced with an open ended question in the form of a form.
# The question in question is: 'Clubs, athletics, and activities participated in during high school & college'
# This question was taken from the Boulder, Colorado IFC On The Hill Rush records.
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import re
import numpy as np
import pandas as pd
import csv

# The response class should be a class that is applied to every cell in a column, it should have methods for cleaning and a gen counts mthod that takes an external dict of word counts or word values
# On __init__, a response should clean itself, with wash_item
class Response:

    def __init__(self, cell_value, column_wordCounts={}, column_wordValues={}):
        # Globals
        self.delimiters = [', ', '\n', ' and ', '. ', '- ', '\\n', '+', '(', ')']
        self.standard_delimiter = ','
        self.removable_punctuation = ['.', '!', '/', '*']

        self.text = self.wash_item(cell_value)
        self.fragments = self.fragment_self()

        if len(column_wordCounts)!=0:
            # print('column_wordCounts was passed, assigning with func.')
            self.fragment_counts = self.assign_fragmented_counts(column_wordCounts)
        else:
            self.fragment_counts = []

        if len(column_wordValues)!=0:
            self.fragment_values = [] # replace with call to assign_fragment_word_values()
        else:
            self.fragment_counts = []

        self.extracted_acs = []
    

    # Recieves a cell_value from __init__
    # converts the text to lowercase, standardizes delimiters, removes punctuation
    # Returns washed item as string
    def wash_item(self, item, v=True):
        if v:
            print('Washing: "{}"'.format(item))
    
        # lower the item
        item = str(item).lower()

        # loop thru known delims and standardize
        for d in self.delimiters:
            item = item.replace(d, self.standard_delimiter)

        # loop through removable punctuation and remove it
        for p in self.removable_punctuation:
            item = item.replace(p,'')

        if v:
            print('Cleaned: "{}"'.format(item))
        return item

    # Returns the .text value split on standard delimiter, result is a list
    def fragment_self(self):
        frags = self.text.split(self.standard_delimiter)

        # OPerforma a couple tests to remove empty fragments and space fragments
        for frag in frags:
            if len(frag) == 0:
                frags.remove(frag)
            if frag == ' ':
                frags.remove(frag)
        
        return frags


    def assign_fragmented_counts(self, word_counts):
        fragmented_counts = []
        for frag in self.fragments: # for each fragment of the response
            frag_words = frag.split(' ') # get a list of words

            # now generate counts for the fragment
            counts = []
            for word in frag_words:
                try:
                    counts.append(word_counts[word])# try to lookup the word in total_word_counts and if found, add the count to the counts array
                except:
                    counts.append(0) # if the word cant be found in total_word_counts, append a "0" to the counts array
            fragmented_counts.append(counts)
        # fragmented counts looks like [[0, 4, 8, 64, 41], [68], [4, 78]]
        return fragmented_counts

    # TODO: Everything. The idea with this is to assign values to certain words either for scoring against other responses or for identifying parents. 
    # Expands on the reasoning about word counts and parent relationship
    def extract_values_by_word_count(self):
        pass

    # Recieves a list of words that should be extracted if found
    # Loops through values_to_extract and searches for the item in the Response.text attribute
    # TODO: Should be able to extract items of any length
    # Returns the found values as a string of words
    def extract_values_by_name(self, values_to_extract):
        # this would return a string of values that appear in values_to_extract and self.text
        # if none are found, returns None
        export = []

        for v in values_to_extract:
            if v in self.text:
                export.append(v)
        
        return " ".join(export)

        



class QColumn:
    
    def __init__(self, column, act_clusters={}, v=False, valueWords=[], auto=False):
        # Import
        import re
        import numpy as np
        
        # Set up globals
        self.delimiters = [', ', '\n', ' and ', '. ', '- ', '\\n', '+', ',', '-', ':']
        self.standard_delimiter = ', '
        self.removable_punctuation = ['.', '!', '/', '*', '(', ')']
        self.null_words = ['high','nan', 'school','hs', "I", "a","about","above","after","again","against","ain","all","am","an","and","any","are","aren","aren't","as","at","be","because","been","before","being",
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
        if len(valueWords) == 0:
            self.valueWords = ['rotc','film','hiking', 'theatre','president', 'lacrosse', 'football', 'club', 'soccer', 'tennis', 'climbing', 'baseball', 'basketball', 'diving', 'nhs', 'engineering', 'track', 'leeds', 'debate', 'hockey', 'spikeball', 'swim', 'deca', 'volleyball', 'spirit', 'golf', 'ski', 'speech', 'cross country', 'skiing', 'waterpolo', 'nhi', 'wrestling', 'rugby', 'water polo', 'swimming', 'skateboarding', 'firefighter', 'letterman', 'fbla', 'work', 'lifeguarding', 'student', 'snowboarding', 'nahs', 'squash', 'tsa', 'yearbook', 'crew', 'boulder freeride', 'band', 'wrestle', 'water', 'biking', 'robotics', 'cross', 'sailing', 'deans leadership fellows', 'america ninja warrior', 'freeride', 'yl', 'martial arts', 'frisbee', 'surf', 'shooting', 'esports']
        else:
            self.valueWords = valueWords
        self.act_clusters = act_clusters

        # Wash
        self.column = self.wash_col(column)

        # Initialize
        self.word_counts = self.gen_total_word_counts(self.column) # This shouldnt be called until after the column has been cleaned. It is producing a lot of ("Club,", "Club ", "club")
        self.responses = self.to_Responses()
        self.gen_fragmented_counts()
        if auto:
            self.auto_cluster(debug_mode=True, v=v)
        else:
            self.guided_cluster(debug_mode=True, v=v)

        self.parents_only = self.get_parents_col()

    # Recieves self
    # loops through each item in the column and makes a Response object out of it
    # Returns list of Response objects of equal length to column
    def to_Responses(self):
        responses = []

        for item in self.column:
            R = Response(item, column_wordCounts=self.word_counts) # Creqate a response object of each cell in the column
            responses.append(R) # append the response object to the list
        
        if len(responses) == len(self.column): # True: all items in column have been converted to Response objects
            return responses
        
        else:
            print('Conversion failed the length check!')


    # Recieves the column as col
    # for each item in the col, converts the item to lowercase, standardizes delimiters, removes punctuation
    # Returns a washed column as a list
    def wash_col(self, col, v=False):
        # Func variables
        standard_delim = self.standard_delimiter
        items_in_col = list(col)
        washedCol = []

        # Iterate over items
        for item in items_in_col:
            if v:
                print('Washing: {}'.format(item))

            # lower the item
            item = str(item).lower()

            # loop thru known delims and standardize
            for d in self.delimiters:
                item = item.replace(d, standard_delim)

            # loop through removable punctuation and remove it
            for p in self.removable_punctuation:
                item = item.replace(p,'')

            item = self.drop_stop_words(item)

            if v:
                print('Cleaned: {}'.format(item))

            washedCol.append(item)


        # convert string back into column
        return washedCol
        

    def gen_act_counts(self, arr=[], from_clusters=False):

        if from_clusters: # %%%---> Case to generate column_wordcounts from clusters. This is more effective for clustering new responses but requires a pre-existing clusters object. This should be the case when used from refine_clusters()
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


    def get_parents_col(self):
        parents_col = []

        for r in self.responses:
            parents_col.append(r.clean_response.strip())
        
        return parents_col

    # Grabs the list of response objects
    # creates a dict with the counts of occurances of delimited response fragments
    # Returns this dict
    def gen_fragment_occurances(self):
        print('Making dictionary of delimited item counts')
        responses = self.responses
        counts = dict()

        # loop thru items in the Response object list to count up the occurances of each fragment
        for response in responses:
            frags = response.fragments
            for frag in frags:
                frag = frag.strip()
                if frag in counts:
                    counts[frag] += 1
                else:
                    counts[frag] = 1
        
        self.fragment_occurances = counts
        return counts


    # Save act clusters to a csv, optional verbose=False by default
    # Returns nothing
    def export_clusters(self, filename, v=False):
        with open(filename, 'w', newline="") as csv_file:  
            writer = csv.writer(csv_file)
            writer.writerow(['parent', 'child'])
            for key, value in self.act_clusters.items():
                writer.writerow([key, value])
        if v:
            print('Export to {} complete'.format(filename))
        else:
            pass

    # TODO: This reads in cluster childeren as a string of a list making it impossible to add to, need a way to read it in as a set
    def import_clusters(self, filename):
        with open(filename) as csv_file:
            reader = csv.reader(csv_file)
            myDict = dict(reader)
        del myDict['parent']
        return myDict


    # Recieves a fragment of a response as frag and the parent item in that fragment
    # Checks for the parent's existance and if True it adds fragment to its children, if False it creates the parent and gives it a child of fragment
    # No return, gets called from elsewhere
    def cluster_frag(self, frag, parent, export=False, outFile='clusters.csv', v=False):

        if parent in self.act_clusters:# True: the parent already exists, increment it
            self.act_clusters[parent].add(frag)
        else: # False: the parent does not exist yet, create it and give it a value of a list with fragment inside
            self.act_clusters[parent] = set(frag)

        if export:
            self.export_clusters(outFile)
        else:
            pass
    
        if v:
            print('"{}" has new child: "{}"'.format(parent, frag))
        else:
            pass


    # Recieves a fragment of a response object, if v is true it will print in verbose mode
    # Makes guesses about which words in a fragment are the parent based on a couple rules
    def guess_keys(self, fragment, v=True):
        findings = []

        if bool(len(fragment.split(' ')) == 1): # True: the fragment is a single word
            self.cluster_frag(fragment, fragment) # cluster it with the word as the parent
            findings.append(fragment)

            if v:
                print('Guessing {} is a parent b/c: Single word fragment'.format(fragment))

        # check to see if "team" or "varsity" are in the fragment
        lfrag = fragment.split(' ')
        if 'varsity' in lfrag: # True: the word varsity is in the frag, the parent is the word after 
            try:
                presumptive_parent_index = lfrag.index("varsity") + 1 # returns index after the word varsity
                self.cluster_frag(fragment, lfrag[presumptive_parent_index])
                findings.append(lfrag[presumptive_parent_index])

                if v:
                    print('Guessing {} is a parent b/c: Follows "varsity"'.format(lfrag[presumptive_parent_index]))
            except:
                pass
        elif 'team' in lfrag:
            try:
                presumptive_parent_index = lfrag.index("team") - 1 # returns index before the word team
                self.cluster_frag(fragment, lfrag[presumptive_parent_index])
                findings.append(lfrag[presumptive_parent_index])

                if v:
                    print('Guessing {} is a parent b/c: Follows "team"'.format(lfrag[presumptive_parent_index]))
            except:
                pass
        else:
            pass

        return findings

            
    # loop thru each fragment of each response and delegate each one as either a parent or a child of a cluster
    def guided_cluster(self, valueWords=[], debug_mode=False, export_on_end=True, v=False):
        if len(valueWords)==0:
            valueWords = self.valueWords

        # Debug stat counters
        manual_classifications = 0
        guess_catches = 0
        discards = 0

        for response in self.responses: # Will iterate over the list of Response objects
            fragments = response.fragments
            findings = set()

            for frag in fragments:
                lfrag = frag.split(' ')

                # This searches for valueWords in each fragment. valueWords lets us specify things to look for that the algorithm might miss
                for vWord in valueWords:
                    if vWord in lfrag:
                        self.cluster_frag(frag, vWord, v=v)
                        findings.add(vWord)
                        # break
                    else:
                        pass
                
                # This searches for existing parents in the fragment. Parents that have already been clustered 
                for k in self.act_clusters:
                    if k.split(' ')[0] in lfrag:
                        self.cluster_frag(frag, k, v=v)
                        findings.add(k)
                        # break
                    else:
                        pass

                guesses = self.guess_keys(frag, v=v)
                if len(guesses) > 0: # True: guess_keys() was successful and found a parent in the fragment
                    findings.add(guesses[0])
                    guess_catches += 1
                    # break
                
                # If we have made it this far, then the fragment doesnt contain an existing parent, or a valueWord and guess_keys() didnt find anything so we should ask for input
                if len(findings) == 0:
                    decision = input('Classify: "{}" \t\t "p" to assign it as its own parent, enter/return to discard fragment, or type a parent to assign it to.'.format(frag))
                    manual_classifications += 1

                    if decision == 'p': # True: user classified this fragment as a parent
                        # Options are that the fragment exists as a parent already, doesnt exist and we need to create it
                        self.cluster_frag(frag, frag, v=v)
                        findings.add(frag)
                        # print('{} added to act_clusters as a parent'.format(frag))
                    
                    elif decision == '': # The empty decisino will be used to discard a fragment
                        discards += 1
                        pass

                    elif decision == 'exit':
                        return
                    
                    elif decision == 'export':
                        self.export_clusters('clusters.csv')
                        pass

                    else: # True: the user made an input, cluster the frag with the decision as the parent
                        self.cluster_frag(frag, decision, v=v)
                        findings.add(decision)
                        # print('Succesfully added {} as a child of {}'.format(frag, decision))

            response.clean_response = " ".join(findings)
            if v:
                # print('Found: {}\t\t\tIn: {}'.format(findings, fragments))
                pass
        
        if export_on_end:
            self.export_clusters('clusters.csv', v=v)
        else:
            pass


        if debug_mode:
            percent_guessed = (len(self.responses) - (manual_classifications + discards)) / len(self.responses)
            print('Function Performace\nResponses: {}\nManual Classifications: {}\nGuessed Parents: {}\nDiscarded Fragments: {}\nPercent of parents detected: {}'.format(len(self.responses), manual_classifications, guess_catches, discards, percent_guessed))
        

    def auto_cluster(self, valueWords=[], debug_mode=False, export_on_end=True, v=False):
        if len(valueWords)==0: # if we are not given a list of value words, use the one we already know
            valueWords = self.valueWords

        # Debug stat counters
        missed_classifications = 0
        guess_catches = 0
        found_parents = 0
        found_vWords = 0
        total_frags = 0

        for response in self.responses: # Will iterate over the list of Response objects
            fragments = response.fragments
            findings = set()

            for frag in fragments:
                total_frags += 1
                lfrag = frag.split(' ')
                abbr = self.abbreviate_fragment(frag)
                # add variables of the fragment that include an abbreviated fragment to catch "national honor" society as "nhs"
                # max_word for the word with the highest value count
                # golden_word for the word with the highest value
                # Search for these in cluster parents and value words

                # This searches for existing parents in the fragment. Parents that have already been clustered 
                for k in self.act_clusters:
                    if k.split(' ')[0] in lfrag: # checks if the first word in the cluster parent appears in the list fragment
                        self.cluster_frag(frag, k, v=v)
                        findings.add(k)
                        found_parents += 1
                        # break
                    elif abbr == k: # True: the abbreviation is a parent in clusters
                        self.cluster_frag(frag, k, v=v)
                        findings.add(k)
                        found_parents += 1
                    else:
                        pass

                # This searches for valueWords in each fragment. valueWords lets us specify things to look for that the algorithm might miss
                for vWord in valueWords:
                    if vWord in lfrag:
                        self.cluster_frag(frag, vWord, v=v)
                        findings.add(vWord)
                        found_vWords += 1
                        # break
                    else:
                        pass
                
                guesses = self.guess_keys(frag, v=v)
                if len(guesses) > 0: # True: guess_keys() was successful and found a parent in the fragment
                    findings.add(guesses[0])
                    guess_catches += 1
                    # break
                
                # If we have made it this far, then the fragment doesnt contain an existing parent, or a valueWord and guess_keys() didnt find anything. We will chock this one up as an L
                if len(findings)==0:
                    missed_classifications += 1


            response.clean_response = " ".join(findings)
            if v:
                # print('Found: {}\t\t\tIn: {}'.format(findings, fragments))
                pass
        
        if export_on_end:
            self.export_clusters('clusters.csv', v=v)
        else:
            pass

        if debug_mode:
            success_rate = (total_frags - missed_classifications) / total_frags
            print('Function Performace\nFragments analyzed: {}\nMissed classifications: {}\nGuessed Parents: {}\nValue Words found: {}\nSuccess Rate: {}'.format(total_frags, missed_classifications, guess_catches, found_vWords, success_rate))
        


    # returns total_word_counts  which looks like {word:(times it showed up)}
    # The return value gets assigned to self.word_counts
    def gen_total_word_counts(self, col):
        # print('Generating column word counts')
        # get the column as one long string
        total_word_counts = {}
        self.col_as_string = ''
        item_count = 0 # using a counter, could also use a len(self.col_as_string.split(" ,., "))
        for item in col:
            item = item.replace(', ', ' ') # this will eliminate seeing duplicates like "club," and "club", The difference is when the word is listed with other words or at the end
            self.col_as_string += str(item)+' ,., ' # use a special delim, " ,., " to later split responses
            item_count += 1

        # all_items = re.findall('\w+', self.col_as_string) # re: returns a list of all words???? what does this accomplish??
        all_items = self.col_as_string.split(' ')
        # print('Length of all_items: '+str(len(all_items)))
        
        words, counts = np.unique(all_items, return_counts=True)
        # print('Words has {} items'.format(len(words)))

        # This loops through the words and counts and turns them into a dictionary 
        for i in range(len(words)):
            if words[i] in self.null_words: # True: the word weare looking at has been identified as a Null word so we want to give it a count of 0 in self.word_counts
                total_word_counts[words[i]] = 0
            else: # False: The word we are looking at is not found in the null_words object so we will continue like normal, g
                total_word_counts[str(words[i])] = counts[i]
            # print('word: {}\tcount: {}'.format(words[i], counts[i]))
        
        #print(self.total_word_counts)
        return total_word_counts
    

    # grabs a list of Response objects from itself
    # Iterates through the list of response objects and sets each objects fragmented_counts attribute based on the column's word_counts dict
    # Doesnt return, fragmented counts looks like [[0, 4, 8, 64, 41], [68], [4, 78]]
    def gen_fragmented_counts(self):
        responses = self.responses

        # for each Response object in responses
        for response in responses:
            fragmented_counts = []
            for frag in response.fragments: # for each fragment of the response
                frag_words = frag.split(' ') # get a list of words

                # now generate counts for the fragment
                counts = []
                for word in frag_words:
                    try:
                        counts.append(self.word_counts[word])# try to lookup the word in total_word_counts and if found, add the count to the counts array
                    except:
                        counts.append(0) # if the word cant be found in total_word_counts, append a "0" to the counts array
                fragmented_counts.append(counts)
            # fragmented counts looks like [[0, 4, 8, 64, 41], [68], [4, 78]]
            response.fragmented_counts = fragmented_counts


    # The goal of this finction is to make an abbreviation of the fragment so that it can be recognizerd even in it's abrreviated form
    def abbreviate_fragment(self, fragment):
        abbr = ''
        words = fragment.split(' ')

        for w in words:
            abbr += w[0]

        return abbr


    # Recieves an identified fragment of a response, that response as a list of words, and counts for those words
    # implements clustering and incrementing of cluster sub_acs as planned
    # Returns the word in the fragment with the highest count
    # Called from clean_by_counts to assign fragment_parent
    def cluster_fragment(self, fragment, words, counts):
        # fragment = an identified fragment of a response
        # words = fragment.split(' ')
        # counts = an array of equal length as words, containing the corresponding word counts for the words in words

        # counts.index(max(counts)) words list at the index for the max value of counts, this
        max_word_in_words = words[counts.index(max(counts))] # this just strips everything that isnt alphanumeric from the word with the highest count
        # ^ needs to be examined as well as the rest of the parameters in this func. I dont think the method of searching our nested list of word counts is working as expected

        # True: the word with the highest count is found in act_clusters as a parent.
        # good chance this is the word we are looking for if it got clustered as an ac_parent
        if max_word_in_words in self.act_clusters: 
            # this is good, continue to see if the entire fragment exists as a child of the now identified ac_parent
            if fragment in self.act_clusters[max_word_in_words]: # True, True: the word with the highest count is found as a parent and the entire fragment is found as a child of max_word
                self.act_clusters[max_word_in_words][fragment] += 2 # add 2 to the occurances of this ac_child in our clusters object, adding 2 because extra points 
            else: # False: the max_word is in act_clusters but fragment is not found as a child. 
                self.act_clusters[max_word_in_words][fragment] = 1 # Create it and give it a count of 1
        else: # False: max_word is not found in act_clusters. create it and make fragment its child with a count of 1
            self.act_clusters[max_word_in_words] = {}
            self.act_clusters[max_word_in_words][fragment] = 1
            
        return max_word_in_words
    

    # So clean!!
    # Recieves a text
    # loops through the words in text and if the word isnt in the global list of null_words, adds it to return list
    # Returns the text with null_words removed
    def drop_stop_words(self, text):
        without = ''
        words = text.split(' ')
        for word in words:
            if word not in self.null_words:
                without += word+' '
            else:
                pass
        return without.strip()
    

    # Gets passed a cell from a DF column
    # Drops stop words, fragments the response, gets fragmented word counts, TODO: find ac_parents based on fragmented counts and return them
    # Returns NOT DONE
    def clean_by_counts(self, resp):
        resp = self.drop_stop_words(resp)
        extracted_acs = set()
        print('Response: {}'.format(resp))
        response_with_frag_counts = self.gen_fragmented_counts(resp)
        print('Fragments: {}'.format(response_with_frag_counts))

        # TODO: read through the fragmented counts and extract the words that need to be returned to the clean cell of only ac_parents
        # TODO: return those words in a string of words

        # DEPRECATED
        # for frag in response_with_frag_counts:
        #     frag_words = frag.split(' ')

        #     # return a list of word counts for corresponding words in frag of fragment
        #     frag_word_counts = self.lookup_fragment_word_counts(frag_words) 

        #     # TODO: This cluster_fragment call probably isnt returning a value as expected, check the func for more details
        #     fragment_parent = self.cluster_fragment(frag, frag_words, frag_word_counts)
        #     print('Fragment parent: {}'.format(fragment_parent))
        #     extracted_acs.add(fragment_parent)
        
        return extracted_acs
        
    # TODO: All of it
    def refine_clusters(self, act_clusters):
        act_clusters = self.act_clusters
        #for ac_parent in act_clusters:
            # sort the sub_acs by frequency, the least frequent sub acs might have the most words and might be worth refining
            # find some way to determine refined parents to look for
            # only allow the most specific refined parent per sub_ac
            # for each refined_parent, search for occurences in sub_acs and and output a new refined sub_ac dict
            # if a refined_parent is found in the sub_ac, isolate it and add it to the refined sub_acs
                # for the sub ac that is not part of the isolated refined sub_ac, do something with it, either delete it or put it somewhere else
                # add occurances of other ac_parents to their respective cluster 
            

    # Recieves a column of a DF 
    # if with_clusters=True it will loop thru the cells in col and apply the clean_with_clusters(), otherwise it will apply the clean_by_counts()
    # Sets self.cleaned_col
    def clean_column(self, col, with_clusters=False):

        if with_clusters: # True: clean the column using the clean_with_clusters() method
            cleaned_col = []
            for response in col:
                cleaned_col.append(self.clean_with_clusters(response, self.act_clusters))
            self.cleaned_col = cleaned_col

        else: # Flase: clean the column using the clean_by_counts() method
            cleaned_col = []
            for response in col:
                
                cleaned_col.append(self.clean_by_counts(response))
            #return cleaned_col
            self.cleaned_col = cleaned_col


    # Recieves a cell of a DF column as resp
    # Looks for each ac_parent of clusters in resp, 
    def clean_with_clusters(self, resp, clusters):
        extracted_acs = []
        resp = resp.split(' ')
        for ac_parent in clusters.keys():
            # if ac_parent in resp:
            try:
                ac_parent_index = resp.index(ac_parent)
                sub_acs = clusters[ac_parent].keys()
                extracted_acs.append(look_for_sub_acs(resp, ac_parent_index, sub_acs)) # Think we should export the ac_parent instead of the sub_ac
            except:
                pass
        return extracted_acs
        
 
    # Recieves a list of words in the cell of a DF as resp, the index of the ac_parent in resp(p1_index) and a list of sub_acs for the found parent
    # 
    def look_for_sub_acs(self, resp, p1_index, sub_acs):

        for sub_ac in sub_acs:
            ac_parent_index = sub_ac.index(resp[p1_index])
            if ac_parent_index == 0:
                #look right
                right = bool(sub_ac[-1] == resp[(len(sub_ac) - ac_parent_index + 1) + p1_index])
                #That line looks for the right most word in the sub ac at it's corresponding index in the response, aligned on the ac_parent
            elif ac_parent_index == (len(sub_ac)-1): # True: ac_parent is found to be the last word of the sub_ac
                left = bool(sub_ac[0] == resp[(p1_index - ac_parent_index)])
                #That line looks for the left most word in the sub ac at the same distance from the ac parent in the resp list, left will be True if they are the same 
            else:
                right = bool(sub_ac[-1] == resp[(len(sub_ac) - ac_parent_index + 1) + p1_index])
                left = bool(sub_ac[0] ==resp[(p1_index - ac_parent_index)])
            if left or right:
                ac_parent = resp[p1_index]
                print('Found {} in response: {}'.format(ac_parent, resp))
                self.act_clusters[ac_parent][sub_ac] += 1
                return sub_ac
            else:
                pass 
        
    def clean_and_cluster_item(self, item, act_clusters, act_counts):
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


                    # if the ac parent is club then we are interested in the sub_ac. (ie: key club, frisbee club, chess club)
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
    
    # Setting self.act_clusters from an outside cluster import
    def set_clusters(self, clusters):
        try:    
            self.act_clusters = clusters
            print('STATUS: Object\'s clusters have been updated!')
        except:
            print('STATUS: Updating object\'s clusters failed!')

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
            notNans = list(filter(lambda a: a != 'NaN', self.cleaned_col))
            l = len(list(filter(lambda a: len(a) > 0, notNans)))
            self.retention = l / len(self.column)
            # retention should be a measure of the percentage of rows in the column that were succesfully clustered
        except:
            pass
        
        # IDEA: Maybe show some metric of the number of the palcement of response's contents within the clusters

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

# %%
