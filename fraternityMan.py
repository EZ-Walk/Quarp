class Fman:
    
    # self.null_words = ['high', 'school', 'played', "I", "a","about","above","after","again","against","ain","all","am","an","and","any","are","aren","aren't","as","at","be","because","been","before","being"]


    def __init__(self, **kwargs):
        # build out attributes as a dict from kwargs
        self.__dict__.update(kwargs)
        try:
            self.full_name = self.__dict__['first_name'] + ' ' + self.__dict__['last_name']
        except:
            self.from_csv = True
        self.member_affinity_dict = {}
    
    def sterilize_response(self, response):
        delimiters = [', ', '\n', ' and ', '. ', '- ']
        punctuaion = {'`', '!', '”', '$', '=', "'", '\\', '^', '+', ',', ')', '}', '_', '"', '#', '<', '[', '-', ';', '|', '.', '(', '%', '/', '?', '&', ':', '@', ']', '*', '~', '“', '{', '>'}
        standard_delim = ', '
        #pass
        # Identify and standardize delimiters
        for delim in delimiters:
            if delim in response: # True: the delimiter is in the response, we should replace it with a ", "
                response = response.replace(delim, standard_delim)
            else:
                pass
        # Delimiters have been standardized

        # create fragments and fragment counts
        # for each fagment, 
        #   convert to all lowercase list of words without punctuation
        #   generate word count array
        fragments = response.split(standard_delim) # Splitting the response on the standard delimiter gives you a list of fragments
        sterile_response = ''
        fragmented_counts = []
        for frag in fragments:
            
            # this for loop removes punctuation from the fragment 
            for char in punctuaion: 
                frag = frag.replace(char,'')

            frag_words = frag.split(' ')
            # frag_words = re.findall('\w+', frag) # fragment words is now a list of words without punctuation
            string_frag = ' '.join(frag_words) # this joins the fragment words around spaces. Result: "i participated in varsity soccer"
            sterile_response += string_frag.lower()+standard_delim # this lowers the fragment_string and adds the standardized delimiter to the end of the string to be rejoined with the rest of the fragements
            # convert to lowercase list of words
            # remove punctuaion
            
            #print('Fragment has been cleaned: {}'.format(frag))
            

            fragment_word_counts = self.gen_fragment_word_counts(string_frag.lower().split(' '))
            fragmented_counts.append(fragment_word_counts)

        return tuple(sterile_response, fragment_word_counts)   
            
        # return sterile_response = {"i participated in varsity soccer, football, key club": [[0, 4, 8, 64, 41], [68], [4, 78]]} This is what a processed response  with fragmented counts should look like.


    def gen_fragment_word_counts(self, words):
        counts = []
        for word in words:
            # counts.append(self.total_word_counts['counts'][int(self.total_word_counts['words'].index(word))]) # this long line adds the count of the word to counts. This can probably be done a better way...
            # print(re.findall('\w+',word))
            try:
                if word in null_words:
                    counts.append(0)
                else:    
                    counts.append(self.word_counts[word.title()])# try to lookup the word in total_word_counts and if found, add the count to the counts array
            except:
                counts.append(0) # if the word cant be found in total_word_counts, append a "0" to the counts array
        return counts


    def score_against_actives(self, actives):

        score_table = {
            'string scoring': {
                'activities': 100,
                'accomplishments': 80,
            },
            
            'exclusive match': {
                'hometown': 20,
                'home_state': 10,
                # 'highschool': 30,
            },
            
            'double match': {
                'year_in_school&major': 15,
                # 'major&dorm_address': 20,
            },
        }

        for mem in actives:
                print('Scoring PNM: '+ str(self.full_name) + '\t against member: ' + str(mem.full_name))
                mem_affinity = 0
                
                try: # to score string scoring values
                    for key in score_table['string scoring']:
                        # print('String scoring, key:' + str(key))
                        mult = score_table['string scoring'][key]
                        similarity = cos_sim(self.__dict__[key], mem.__dict__[key])

                        mem_affinity += mult * similarity
                except:
                    print('Failed to score strings')
                        
                for key in score_table['exclusive match']:
                    if self.__dict__[key] == mem.__dict__[key]:
                        mem_affinity += score_table['exclusive match'][key]
                    else:
                        pass
                
                for st_key in score_table['double match']:
                    key1, key2 = st_key.split('&') # this statement seperates the score_table key into the 2 keys we are going to try to match
                    # print('Scoring, double match: {} and {}'.format(key1, key2))
                    cond1 = self.__dict__[key1] == mem.__dict__[key1]
                    cond2 = self.__dict__[key2] == mem.__dict__[key2]
                    
                    if cond1 and cond2:
                        mem_affinity += score_table['double match'][st_key]
                    
                if mem_affinity > 0:
                    print('{}\'s affinity to {} is {}'.format(self.full_name, mem.full_name, mem_affinity))
                    self.member_affinity_dict[mem.full_name] = mem_affinity
                else:
                    print('This PNM has 0 affinity with this member')
                    pass # this PNM has no affinity to this member, so we should skip adding it to the member_affinity_dict
                print()

    def export_attributes(self):
        return self.__dict__