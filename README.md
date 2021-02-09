# Text Similarity

This is an api that implements several text similarity algorithms. 

#### Running the API

1. Make sure docker is properly installed `https://docs.docker.com/install/`
2. Clone the repo
3. cd into cloned directory
4. `docker build -t text-similarity . && docker run --rm -p 80:80 text-similarity`

### Usage

The api accepts two text passages, and scores them in similarity from 0.0 (completely dissimilar) to 1.0 (the same).

Here's some example usages

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
