# 2019 iGem Outreach Database

## How to Use

### 1. Install Dependencies

### 2. Run Web Scraper
The scraper (dataScraperHeadToP.py) takes in a list of urls in the format of (toScrape.csv) and then outputs data (check initial_data.csv) in the data folder.  Summarization can be done using the summarize_bert.py script.  

### 3. Use Machine Learning Model
Run the code in database_machine_learning.ipynb. It trains machine learning model using data from 2015 to 2017 (edited_data.csv), and labels events in 2018 based on their descriptions. The output data are store in 2015-2018 data final.csv

## 1. Motivation

With hundreds of iGEM teams developing innovative pedagogical tools and outreach practices for synthetic biology, there is an obvious need for a database similar to the iGEM Parts Registry that promotes dissemination of teams' outreach projects. This database should document these achievements and be easily searchable to promote widespread accessibility so future teams could draw inspiration from past projects to better serve their communities. To facilitate this process, the W&M iGEM team created an outreach database in 2017 and manually updated it in 2018. However, updating via manual curation was a major challenge, which requires over 600 man-hours each year. It is inefficient and not in line with available technology. The question of how to keep databases updated and current actually dissuades iGEM teams from constructing databases for other iGEM activities (e.g. modeling), despite the usefulness of these databases for the community.

To address this problem, we created software to automate this process through the use of groundbreaking web scraping and machine learning techniques. Specifically, our web scraper is able to visit team sites, locate relevant pages, and group and extract contents from different pages. Our learning models can summarize the events, then identify their audiences, categories, and goals based on automatically collected textual descriptions. This software will obviously be beneficial for the teams that utilize it to improve their own outreach projects in future years. Equally important, our software will hopefully provide the framework for future teams who are considering making a searchable database to make other aspects of iGEM teams' projects more accessible to the community.

## 2.Web Scraping

In order to automatically collect teams' data, we wanted to use web scraping to visit team sites and collect relevant data about successful outreach events that happened in 2018. In our initial scraper, we used Python, urllib,and beautifulsoup (with lxml). With the urllib library, we could make requests to specific URLs and download the page source, then parse it using beautifulsoup.

We tested various data extraction formats on several pages. Ultimately, we decided that because of the variety of different website styles, the best way to group text together was by header text and content text. Header text would be denoted by a <hx> tag, where x could be any number from 1-6, and the content would be all paragraph (<p>) tags immediately following until the end of the page, or the next header. We would search the HTML tree and find the header tags, then iterate through the sibling tags, matching headers to content. However, this content was often extremely lengthy, so we used the bert extractive summarizer- a pre-trained natural language processing summarization library - to generate a shorter summary of the descriptions.
  
 Once we found an extraction model that worked, we sought to expand our web scraper’s capabilities. An issue we found while using urllib was its inability to handle dynamic javascript heavy web pages. This library only downloaded the HTML source code as-is, and thus wouldn’t get any HTML loaded in from javascript. To combat this obstacle, we switched to selenium, an auto web page testing software. We used Seleniumto drive Google Chrome, and this way, we would be able to handle javascript events and thus get the full content of every webpage we visited. Essentially, we would visit sites, then wait for all javascript events to conclude before downloading the page source.

The next step was then to have the scraper be able to reach the outreach pages of interest. To facilitate this, our script would interact with the navigation bar on websites and identify the integrated human practices page, and the education and public engagement page. It would then visit and scrape these two pages. Once our scraper had all the capabilities we wanted, we still needed the awards data on each team, as well as the wiki links. Fortunately, we located the JSON source of the iGEM awards page, and we could then use pandas to merge this data with the downloadable team info data, and acquire the team URLs. With a list of URLs, we had our web scraper read our link data and visit each site. Then, it outputs a .csv file containing data matched from header to content.

Although this scraping model failed on some sites where data was encoded into images, rather than text, we can read the images manually because these sites were few. But if there were many sites with this issue, a solution would be to train and deploy an optical character recognition algorithm in order to extract meaning from the images. Furthermore, there were also a few pages where the data was not separated very well, due to these pages being contiguous blocks of text, rather than being organized by sections. These sites are not huge issues, as the text is still extracted, and they only suffer from slightly lower accuracy when sent to the text analysis neural network.

## 3. Machine Learning 

We developed machine models that can automatically label successful outreach events that happened in 2018 based on their descriptions. Our learning models were trained and tested on 2155 outreach events from 2015 to 2017, which were manually labeled by the past iGEM members of W&M. We divided these events into test sets, validation sets, and training sets in a ratio of 0.15:0.15:0.7. Our training and testing data are input-output examples, in which the inputs are event descriptions and the outputs are labels of each event. In our database, there are 3 categories of labels to be classified, which are project tags, audiences, and goals. Thus, we need 1 machine learning model for each category. “Project Tags” describe the contents of an event; there are 16 different tags in total, and each event has one or more tags. “Audiences” categorize the main types of the audience of an event; there are 11 different types of audiences in total, and each event can be associated with one or more types of audiences. “Goals” represent the aims of an event; there are 13 different types of goals in total, and each event has one or more goals. In short, we build 3 learning models to solve 3 multi-label classification problems.

## 1. Data Cleaning
Several things need to be done before we could build our machine learning models. To begin with, we needed to clean up the training and test data.
(a) We dropped the event with missing labels.
(b) We standardized the output labels: labels using different words but having the same meaning are unified into the same words, and transferred labels to binary vectors.
(c) We normalized the input (event descriptions) by deleting meaningless symbols ({ }, ( ), @, #, etc.), removing stop wordsand stemming.

## 2. Word Embeddings
After cleaning, we performed word embedding on our event descriptions. After trying different embedding models such as skip-gram, continuous bag-of-words, and GloVe, we decided to use TF-IDF of bigrams for both classification accuracy and performance considerations.

## 3. Training and Testing Models 
Once the data was prepared, we were ready to implement machine learning models for classification. We tried lots of learning algorithms, such as random forests, gradient boosting, neural networks, ridge regression, etc. The best models we have built are using C-SVM with classifier chains. These models got amazing classification results on the test set, with an accuracy of 95.20% for labeling the “Project Tags”, an accuracy of 93.25% for labeling the “Audiences”, and an accuracy of 92.11% for labeling the “Goals”.

Accuracies were measured by counting the percentages of correct labels. For instance, if we only consider the “Audiences" of one outreach event, 11 possible types of audiences can be associated with this event, and the correct labeling is audience type 3, type 4, and type 5. But if our model only labels type 3 and type 4 for this event, it gets an accuracy of 10/11, because it only labels type 5 wrong. All the other labels are either correct labeled (type 3 and 4) or correct unlabeled (type 1,2,6,7,8,9,10,11). Some people might argue that if this model did not label anything to each event, the accuracy would still be high, because the model correctly “unlabeled” many labels. This is true, but it does not mean that our C-SVM models are not good. Because if we set the output of our models to be all zeros, we got an accuracy of 78.1% for labeling the “Project Tags”, an accuracy of 77.3% for labeling the “Audiences”, and an accuracy of 77.5% for labeling the “Goals”. We also measured that 51.6% of events have all the “Project Tags” correctly labeled, 51.2% of events have all the “Audiences” correctly labeled, and 50.9% of events have all the “Goals” correctly labeled. Thus, our models do recognize important features within the text and assign accurate labels.

## 4. Final Results
After cleaning up the event descriptions collected by our web scraper and performing word embedding for them, we could use our learning models to label these autonomously collected data.

## 5. Future Considerations
There are ways to further improve the multi-label classification accuracies. For example, if we have more data to train our deep learning models and find better ways to construct different layers, we can achieve much higher accuracy than the current neural network models do. Besides, advanced embedding models (e.g. GloVe and continuous bag-of-words) usually work better than simple models such as bag-of-words and TF-IDF. We did not choose advanced models because they took a very long time to embed descriptions and train our learning models. But, given more time to study advanced embedding models and optimize our implementations, we are confident that we can speed up the training process.

