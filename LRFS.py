{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "LRFS.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "authorship_tag": "ABX9TyOItEqfedW3LqtnYdHkhZL5",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/thedataninja1786/Data-Mining/blob/main/LRFS.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "yJCHwtgGEMno"
      },
      "source": [
        "#TEXT PREPROCESSING AND CLASSIFICATION FROM SCRATCH"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "3F38JN3yEGdI",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "423be623-548f-4e0f-b1cb-5e54ac336aaa"
      },
      "source": [
        "#Import necessary modules \r\n",
        "import nltk\r\n",
        "import re \r\n",
        "import string \r\n",
        "import pandas as pd \r\n",
        "import numpy as np \r\n",
        "nltk.download('twitter_samples')\r\n",
        "nltk.download('stopwords')\r\n",
        "from nltk.corpus import stopwords\r\n",
        "from nltk.corpus import twitter_samples\r\n",
        "positive_tweets =twitter_samples.strings('positive_tweets.json')\r\n",
        "negative_tweets =twitter_samples.strings('negative_tweets.json')"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "[nltk_data] Downloading package twitter_samples to /root/nltk_data...\n",
            "[nltk_data]   Package twitter_samples is already up-to-date!\n",
            "[nltk_data] Downloading package stopwords to /root/nltk_data...\n",
            "[nltk_data]   Package stopwords is already up-to-date!\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "slpohuQJHKCo"
      },
      "source": [
        "#Load the train and test data \r\n",
        "positive_tweets =twitter_samples.strings('positive_tweets.json')\r\n",
        "negative_tweets =twitter_samples.strings('negative_tweets.json')\r\n",
        "\r\n",
        "positive_train_tweets = positive_tweets[:4000]\r\n",
        "positive_test_tweets = positive_tweets[4000:]\r\n",
        "negative_train_tweets = negative_tweets[:4000]\r\n",
        "negative_test_tweets = negative_tweets[4000:]\r\n",
        "\r\n",
        "#Assign label 1 for positive tweets and 0 for negative tweets\r\n",
        "positive_df = pd.DataFrame(positive_train_tweets) \r\n",
        "positive_df['label'] = 1 \r\n",
        "negative_df =   pd.DataFrame(negative_train_tweets)\r\n",
        "negative_df['label'] = 0 \r\n",
        "df = pd.concat([positive_df ,negative_df], axis = 0 )\r\n",
        "df = df.reset_index(drop=True)\r\n",
        "df=df.rename(columns = {0:'text'})"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "ke8GfPtwEmfO"
      },
      "source": [
        "##Define the functions for prepocessing text, creating sequences and padding"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "SZ8xSFOK5_7A"
      },
      "source": [
        "def remove_URL(text): #remove urls\r\n",
        "  url = re.compile(r'https?://\\S+|www\\.\\S+')\r\n",
        "  return url.sub(r\"\",text)\r\n",
        "\r\n",
        "def remove_punct(text): #remove punctuations \r\n",
        "  translator = str.maketrans(\"\",\"\",string.punctuation)\r\n",
        "  return text.translate(translator)\r\n",
        "\r\n",
        "stop_words = set(stopwords.words('english')) \r\n",
        "\r\n",
        "def remove_stopwords(text): #remove stopwords \r\n",
        "  filtered_words = [word.lower() for word in text.split() if word.lower() not in stop_words]\r\n",
        "  return \" \".join(filtered_words)\r\n",
        "\r\n",
        "def count_frequency(df,text): #count the frequency of each word \r\n",
        "  freq_dict = {}\r\n",
        "  for row in df[text]:\r\n",
        "    for word in row.split(): #tokenize\r\n",
        "      if word not in freq_dict:\r\n",
        "        freq_dict[word] = 1 \r\n",
        "      else:\r\n",
        "        freq_dict[word] += 1\r\n",
        "  return freq_dict \r\n",
        "\r\n",
        "def find_unique_words(df,text): # find the unique words\r\n",
        "  all_unique_words = []\r\n",
        "  for row in df[text]:\r\n",
        "    for word in row.split():\r\n",
        "      if word not in all_unique_words:\r\n",
        "        all_unique_words.append(word)\r\n",
        "  all_unique_words = sorted(list(set(all_unique_words)))\r\n",
        "  return all_unique_words\r\n",
        "\r\n",
        "def index_assignment(all_unique_words): #assign index to each word\r\n",
        "  index_dict = {}\r\n",
        "  count = 0 \r\n",
        "  for word in all_unique_words:\r\n",
        "    count += 1 \r\n",
        "    index_dict[word] = count \r\n",
        "  return index_dict\r\n",
        "\r\n",
        "def text_to_sequences(df,text,index_dict): #convert text to sequence\r\n",
        "  text_sequences = []\r\n",
        "  for row in df[text]:\r\n",
        "    empty = []\r\n",
        "    for word in row.split():\r\n",
        "      empty.append(index_dict.get(word))\r\n",
        "    text_sequences.append(empty)\r\n",
        "  return text_sequences\r\n",
        "\r\n",
        " \r\n",
        "def padded_sequences(text_sequences:list): #pad sequences\r\n",
        "  padded_sequences = []\r\n",
        "  max_len = 30 #choose an arbritrary number \r\n",
        "  for text_sequence in text_sequences:\r\n",
        "    length = len(text_sequence)\r\n",
        "    i = 0 \r\n",
        "    while  length + i < max_len:\r\n",
        "      text_sequence.insert(i,0)\r\n",
        "      i += 1\r\n",
        "    padded_sequences.append(text_sequence)\r\n",
        "  return padded_sequences "
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "z7fDl0LX69Il"
      },
      "source": [
        "#Apply the functions to the thraining data \r\n",
        "df['text']  = df['text'].apply(lambda x : remove_URL(x))\r\n",
        "df['text']  = df['text'].apply(lambda x : remove_punct(x))\r\n",
        "df['text']  = df['text'].apply(lambda x : remove_stopwords(x))\r\n",
        "frequencey_dict = count_frequency(df,'text')\r\n",
        "unique_words = find_unique_words(df,'text')\r\n",
        "index_dictionary = index_assignment(unique_words)\r\n",
        "train_sequences = text_to_sequences(df,'text',index_dictionary)\r\n",
        "train_padded = padded_sequences(train_sequences)"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "t0RTcfTqFErb"
      },
      "source": [
        "##Classify text using Logistic Regression "
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "fESgOov6DBdr",
        "outputId": "59f5c86e-4069-4515-989f-50e051cd7936"
      },
      "source": [
        "#Initialize the wights vector \r\n",
        "weights = []\r\n",
        "for _ in range(30):\r\n",
        "  weights.append(1/30)\r\n",
        "\r\n",
        "#Training the model \r\n",
        "predictions = []\r\n",
        "bias = 0.5\r\n",
        "lr = 0.0001\r\n",
        "m = 1 / len(train_padded[0])\r\n",
        "\r\n",
        "for i,element in enumerate(train_padded):\r\n",
        "  derivatives = []\r\n",
        "  prediction = 0 \r\n",
        "  actual = df['label'][i]\r\n",
        "  for j,pad in enumerate(element):\r\n",
        "    prediction += pad * weights[j]\r\n",
        "  prediction += bias \r\n",
        "  sigmoid = 1 / (1 + np.exp(-prediction)) \r\n",
        "  predictions.append(round(sigmoid))\r\n",
        "\r\n",
        "  for i in range(len(weights)):\r\n",
        "    dw = (1/m) * (element[i] * (sigmoid - actual)) * lr \r\n",
        "    derivatives.append(dw)\r\n",
        "\r\n",
        "  for i,derivative in enumerate(derivatives):\r\n",
        "    weights[i] -= derivative \r\n",
        "  \r\n",
        "  db = (1/m) * (sigmoid - actual) * lr\r\n",
        "\r\n",
        "  bias -= db\r\n",
        "\r\n",
        "df['predictions'] = predictions\r\n",
        "\r\n",
        "print('Accuracy is: ' + str(df['label'].sum() / df['predictions'].sum()))"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "/usr/local/lib/python3.6/dist-packages/ipykernel_launcher.py:15: RuntimeWarning: overflow encountered in exp\n",
            "  from ipykernel import kernelapp as app\n"
          ],
          "name": "stderr"
        },
        {
          "output_type": "stream",
          "text": [
            "Accuracy is: 0.9982530571499876\n"
          ],
          "name": "stdout"
        }
      ]
    }
  ]
}