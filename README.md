# Text Similarity

This is an api that implements several text similarity algorithms. 

#### Running the API

1. Make sure docker is properly installed `https://docs.docker.com/install/`
2. Clone the repo
3. cd into cloned directory
4. `docker build -t text-similarity . && docker run --rm -p 80:80 text-similarity`

### Usage

The api accepts two text passages, and scores them in similarity from 0.0 (completely dissimilar) to 1.0 (the same).

Here's some example usages, navigate to a second terminal to use as a client.

A text compared to itself:

`curl -i -X POST localhost:80/Similarity -H "Content-Type: application/json" --data "@test-data/same-texts.json"`

A text compared to a similar text:

`curl -i -X POST localhost:80/Similarity -H "Content-Type: application/json" --data "@test-data/similar-texts.json"`

A text compared to a less similar text:

`curl -i -X POST localhost:80/Similarity -H "Content-Type: application/json" --data "@test-data/less-similar-texts.json"`

By specifying a Model parameter in the Metadata object of the request, the user can explicitly choose between the three models. The options available are "Cos", "Intersection", and "KLD". "Cos" is used as the default if a model is not explicitly specified, as in the examples above.

An example using the intersection algorithm:

`curl -i -X POST localhost:80/Similarity -H "Content-Type: application/json" --data "@test-data/similar-texts-intersection.json"`

And one using the Kullback-Liebler divergence:

`curl -i -X POST localhost:80/Similarity -H "Content-Type: application/json" --data "@test-data/similar-texts-kld.json"`

### Modeling

Here's brief write-ups detailing the functionality of the three models.

#### Intersection

Processes the two texts to create sets of unique words. It then calculates the cardinality of the intersection of the sets divided by the cardinality of union the sets.

#### KLD

For words that are in both of the texts, calculates a vector where each entry is the count for one of the unique words. Treating each of these vectors as a histogram-like distribution, then calculates the Kullback-Liebler divergence of the two distributions. Finally, calculates the intersection metric, and divides that by 1 plus the KL Divergence. This value can distinguish two sentences that use all the same words, but have differing counts of these words. 

#### Cos

Calculates vectors of word counts similarly to the KLD metric. Returns the cosine of the angle between these vectors, calculated using dot products. Identical texts will receive a value of 1, because the angle between the count vectors will be 0. Texts that share no words in common will give orthogonal vectors, and thus return a similarity of zero. This model was chosen as the default because it varies in a smooth and predictable way as words are modified in the sentences.

