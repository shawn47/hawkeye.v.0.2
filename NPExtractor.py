# coding=UTF-8
import nltk
from nltk.corpus import brown

# This is a fast and simple noun phrase extractor (based on NLTK)
# Feel free to use it, just keep a link back to this post
# http://thetokenizer.com/2013/05/09/efficient-way-to-extract-the-main-topics-of-a-sentence/
# Create by Shlomi Babluki
# May, 2013


# This is our fast Part of Speech tagger
#############################################################################
brown_train = brown.tagged_sents(categories='news')
regexp_tagger = nltk.RegexpTagger(
    [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
     (r'(-|:|;)$', ':'),
     (r'\'*$', 'MD'),
     (r'(The|the|A|a|An|an)$', 'AT'),
     (r'.*able$', 'JJ'),
     (r'^[A-Z].*$', 'NNP'),
     (r'.*ness$', 'NN'),
     (r'.*ly$', 'RB'),
     (r'.*s$', 'NNS'),
     (r'.*ing$', 'VBG'),
     (r'.*ed$', 'VBD'),
     (r'.*', 'NN')
     ])
unigram_tagger = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)
bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)
#############################################################################


# This is our semi-CFG; Extend it according to your own needs
#############################################################################
cfg = {}
cfg["NNP+NNP"] = "NNP"
cfg["NN+NN"] = "NNI"
cfg["NNI+NN"] = "NNI"
cfg["JJ+JJ"] = "JJ"
cfg["JJ+NN"] = "NNI"


#############################################################################


class NPExtractor(object):
    def __init__(self, sentence):
        self.sentence = sentence

    # Split the sentence into singlw words/tokens
    def tokenize_sentence(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        return tokens

    # Normalize brown corpus' tags ("NN", "NN-PL", "NNS" > "NN")
    def normalize_tags(self, tagged):
        n_tagged = []
        for t in tagged:
            if t[1] == "NP-TL" or t[1] == "NP":
                n_tagged.append((t[0], "NNP"))
                continue
            if t[1].endswith("-TL"):
                n_tagged.append((t[0], t[1][:-3]))
                continue
            if t[1].endswith("S"):
                n_tagged.append((t[0], t[1][:-1]))
                continue
            n_tagged.append((t[0], t[1]))
        return n_tagged

    # Extract the main topics from the sentence
    def extract(self):

        tokens = self.tokenize_sentence(self.sentence)
        tags = self.normalize_tags(bigram_tagger.tag(tokens))

        merge = True
        while merge:
            merge = False
            for x in range(0, len(tags) - 1):
                t1 = tags[x]
                t2 = tags[x + 1]
                key = "%s+%s" % (t1[1], t2[1])
                value = cfg.get(key, '')
                if value:
                    merge = True
                    tags.pop(x)
                    tags.pop(x)
                    match = "%s %s" % (t1[0], t2[0])
                    pos = value
                    tags.insert(x, (match, pos))
                    break

        matches = []
        for t in tags:
            if t[1] == "NNP" or t[1] == "NNI":
                # if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN":
                matches.append(t[0])
        return matches


# Main method, just run "python np_extractor.py"
def main():
    # sentence = "Swayy is a beautiful new dashboard for discovering and curating online content."
    sentence = "WASHINGTON/BEIJING (Reuters) - The Trump administration’s top two negotiators in trade talks with China will meet on Friday with Chinese President Xi Jinping, but there has been no decision to extend a March 1 U.S. deadline for a deal, White House economic adviser Larry Kudlow said on Thursday. “The vibe in Beijing is good,” Kudlow told Fox News Channel of the U.S.-China talks that are set to conclude on Friday in Beijing. But Kudlow’s upbeat assessment contrasted with reports from two people familiar with the talks, who said progress has been difficult on the thorniest issues involving U.S. demands that China make sweeping changes to curb forced technology transfers and to enforce intellectual property rights. Sources briefed on the talks also told Reuters that China had pledged to make its industrial subsidy programs compliant with World Trade Organization rules and end those that distort markets, but had offered no details on how it intends to achieve that goal. The offer has been met with skepticism from U.S. negotiators, in part because China has long refused to disclose its subsidies. Negotiators from the two sides are pushing to de-escalate a tariff war that has dimmed global growth forecasts, roiled financial markets and disrupted manufacturing supply chains. U.S. tariffs on $200 billion worth of imports from China are scheduled to rise to 25 percent from 10 percent if the two sides do not reach a deal by March 1, increasing pressure and costs in sectors from consumer electronics to agriculture. Although U.S. President Donald Trump said earlier this week that an extension of the deadline was possible if a “real deal” was close, Kudlow, director of the National Economic Council, said the White House had made no such decision. The talks, scheduled to run through Friday, follow three days of deputy-level meetings to work out technical details, including a mechanism for enforcing any trade agreement. China proposed in the talks this week to increase purchases of U.S. semiconductors to $200 billion over six years as part of a deal to ease American tariffs, a person briefed on the talks told Reuters. But the semiconductor proposal, first reported by the Wall Street Journal, was part of a “recycled” package of goods purchase offers that Beijing first presented in the spring of 2018, the source said. CANCELED ORDERS China has also offered to sharply increase purchases of U.S. soybeans and other farm and energy commodities to help cut the U.S. trade deficit, which exceeded $382 billion in 2018. News that Chinese buyers had canceled some recent orders for U.S. soybeans caused Chicago grain futures prices to tumble on Thursday , while negative sentiment weighed on U.S. stocks, keeping major indexes in negative territory. U.S. Trade Representative Robert Lighthizer and Treasury Secretary Steven Mnuchin opened high-level talks Thursday at the Diaoyutai state guest house with Chinese Vice Premier Liu He, the top economic adviser to Chinese President Xi. Trump told reporters on Wednesday that the negotiations had been progressing “very well.” A Bloomberg report cited sources as saying Trump was considering pushing back the deadline by 60 days to give negotiators more time after the Chinese side requested a 90-day extension. U.S. Treasury Secretary Steven Mnuchin, a member of the U.S. trade delegation to China, leaves a hotel in Beijing for talks with Chinese officials, China, February 14, 2019. REUTERS/Thomas Peter But a source familiar with the talks told Reuters on Wednesday, before the high-level talks began, that the Chinese had not raised the idea of a 90-day extension. Hu Xijin, editor-in-chief of China’s nationalist Global Times tabloid, also tweeted that speculation on an extension was “inaccurate,” citing a source close to the talks. Chinese Commerce Ministry spokesman Gao Feng told reporters he had no information on the trade talks’ progress. Trump has said he did not expect to meet with Xi before March 1, but White House spokeswoman Sarah Sanders has raised the possibility of a meeting between the leaders at the president’s Mar-a-Lago retreat in Florida. Chinese Foreign Ministry spokeswoman Hua Chunying said she noted Trump had said many times he wished to meet with Xi, and that China was willing to maintain “close contact” with the U.S. side, but said she had no information to share on any visit by the Chinese president. TRADE GAP NARROWS The Chinese government has offered few details about the state of negotiations this week. Chinese January trade data released on Thursday showed imports from the United States fell 41.2 percent from a year earlier to $9.24 billion, the lowest amount in dollar terms since February 2016. Exports to the United States also declined 2.4 percent to $36.54 billion, the lowest amount since last April. Slideshow (2 Images) China’s trade surplus with the United States narrowed to $27.3 billion in January, from $29.87 billion in December. China’s soybean imports fell 13 percent in January from a year earlier, customs data showed, as a hefty duty on shipments from the United States, its second largest supplier, curbed purchases."
    np_extractor = NPExtractor(sentence)
    result = np_extractor.extract()
    print("This sentence is about: %s" % ", ".join(result))


if __name__ == '__main__':
    main()