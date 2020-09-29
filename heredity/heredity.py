import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    def no_of_genes(person, one_gene, two_genes):
        if person in one_gene:
            return 1
        elif person in two_genes:
            return 2
        else:
            return 0
    
    def trait_type(person, have_trait):
        if person in have_trait:
            return True
        else:
            return False
    
    def from_parent(parent_gene):
        if parent_gene == 0:
            return ((0.01*0.5) + (0.01*0.5))
        elif parent_gene == 2:
            return ((0.99*0.5) + (0.99*0.5))
        else:
            return ((0.5*0.99) + (0.5*0.01))
        
    prob = 1    
    
    for i in set(people):
        gene = no_of_genes(i, one_gene, two_genes)
        trait = trait_type(i, have_trait)
        trait_prob = PROBS["trait"][gene][trait]
        gene_prob = 0
        
        if (people[i]['mother'] == None) and (people[i]['father'] == None):
            gene_prob = PROBS["gene"][gene]
        else:
            from_mom = 0
            from_dad = 0
            mom_gene = no_of_genes(people[i]['mother'], one_gene, two_genes)
            dad_gene = no_of_genes(people[i]['father'], one_gene, two_genes)
            from_mom = from_parent(mom_gene)
            from_dad = from_parent(dad_gene)
            if gene == 1:
                gene_prob = (from_mom)*(1-from_dad) + (from_dad)*(1-from_mom)
            elif gene == 0:
                gene_prob = (1-from_mom)*(1-from_dad)
            else:
                gene_prob = (from_mom)*(from_dad)
                
        prob = (prob)*(gene_prob)*(trait_prob)
        
    return prob
    #raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    def no_of_genes(person, one_gene, two_genes):
        if person in one_gene:
            return 1
        elif person in two_genes:
            return 2
        else:
            return 0
    
    def trait_type(person, have_trait):
        if person in have_trait:
            return True
        else:
            return False
        
    for i in set(probabilities):
        gene = no_of_genes(i, one_gene, two_genes)
        trait = trait_type(i, have_trait)
        probabilities[i]["gene"][gene] += p
        probabilities[i]["trait"][trait] += p
    #raise NotImplementedError

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for i in set(probabilities):
        gene_x = 1/(probabilities[i]["gene"][0]+probabilities[i]["gene"][1]+probabilities[i]["gene"][2])
        trait_x = 1/(probabilities[i]["trait"][True]+probabilities[i]["trait"][False])
        probabilities[i]["gene"][0] *= gene_x
        probabilities[i]["gene"][1] *= gene_x
        probabilities[i]["gene"][2] *= gene_x
        probabilities[i]["trait"][True] *= trait_x
        probabilities[i]["trait"][False] *= trait_x
    #raise NotImplementedError


if __name__ == "__main__":
    main()
