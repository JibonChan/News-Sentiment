import pickle
import re

def cleanInputText(text):
    text = text.lower()
    text = re.sub("@[A-Za-z0-9_]+","", text)
    text = re.sub("#[A-Za-z0-9_]+","", text)
    text = re.sub(r"http\S+","", text)
    text = re.sub(r"www.\S+","", text)
    text = re.sub('[()!?]'," ", text)
    text = re.sub('\[.*?\]'," ", text)
    text = re.sub("[^a-z0-9]"," ", text)
    return text

def main():
    print("Loading the Logistic Regression Model...")

    model = ''
    # with open('sentiment_model.sav','rb') as f:
    #     model = f.read()
    model = pickle.load(open('sentiment_model.sav','rb'))
    print("Successfully Loaded Logistic Regression Model...")

    print("Failed to load Logistic Regression Model !")

    while 1:
        text = cleanInputText(input("Enter Sentence: "))
        nT = [text]
        print(nT)
        print(model.predict(nT))

if __name__ == main():
    main()