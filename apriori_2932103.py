import argparse
import csv
from itertools import combinations


def load_transactions(filename):
    transactions = []

    with open(filename, "r") as file:
        reader = csv.reader(file)

        for row in reader:
            transaction = set()

            for item in row:
                item = item.strip()

                if item:
                    transaction.add(item)

            if transaction:
                transactions.append(transaction)

    return transactions


def find_frequent_1_itemsets(transactions, min_support):
    item_counts = {}

    for transaction in transactions:
        for item in transaction:
            itemset = frozenset([item])
            item_counts[itemset] = item_counts.get(itemset, 0) + 1

    frequent_1 = {}

    for itemset, count in item_counts.items():
        if count >= min_support:
            frequent_1[itemset] = count

    return frequent_1


def has_infrequent_subset(candidate, prev_frequent_itemsets):
    prev_set = set(prev_frequent_itemsets.keys())
    k = len(candidate)

    for subset in combinations(candidate, k - 1):
        if frozenset(subset) not in prev_set:
            return True

    return False


def apriori_gen(prev_frequent_itemsets):
    candidates = []

    prev_itemsets = list(prev_frequent_itemsets.keys())
    length = len(prev_itemsets)

    for i in range(length):
        for j in range(i + 1, length):

            l1 = sorted(list(prev_itemsets[i]))
            l2 = sorted(list(prev_itemsets[j]))

            if l1[:-1] == l2[:-1]:

                candidate = frozenset(set(l1) | set(l2))

                if not has_infrequent_subset(candidate, prev_frequent_itemsets):

                    if candidate not in candidates:
                        candidates.append(candidate)

    return candidates


def count_candidates(transactions, candidates, min_support):
    candidate_counts = {}

    for transaction in transactions:
        for candidate in candidates:

            if candidate.issubset(transaction):
                candidate_counts[candidate] = candidate_counts.get(candidate, 0) + 1

    frequent_itemsets = {}

    for candidate, count in candidate_counts.items():
        if count >= min_support:
            frequent_itemsets[candidate] = count

    return frequent_itemsets


def apriori(transactions, min_support):
    all_frequent_itemsets = []

    L1 = find_frequent_1_itemsets(transactions, min_support)
    all_frequent_itemsets.append(L1)

    while True:

        prev_frequent = all_frequent_itemsets[-1]

        if not prev_frequent:
            break

        candidates = apriori_gen(prev_frequent)

        if not candidates:
            break

        next_frequent = count_candidates(
            transactions,
            candidates,
            min_support
        )

        if not next_frequent:
            break

        all_frequent_itemsets.append(next_frequent)

    return all_frequent_itemsets

def print_results(all_frequent_itemsets, input_file, min_support):

    print("Input file:", input_file)
    print("Minimum support:", min_support)

    all_sets = []

    for level in all_frequent_itemsets:
        for itemset, count in level.items():
            all_sets.append((itemset, count))

    filtered_sets = []

    for itemset, count in all_sets:

        remove = False

        # Remove only single-item subsets
        if len(itemset) == 1:

            for other_itemset, _ in all_sets:

                if len(other_itemset) > 1 and itemset.issubset(other_itemset):
                    remove = True
                    break

        if not remove:
            filtered_sets.append((itemset, count))

    # Print results
    for itemset, count in sorted(
        filtered_sets,
        key=lambda x: (len(x[0]), sorted(x[0]))
    ):
        print(set(itemset), ":", count)

    print("\nTotal number of frequent itemsets:", len(maximal_itemsets) + 1)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input CSV file"
    )

    parser.add_argument(
        "-m",
        "--minsup",
        required=True,
        type=int,
        help="Minimum support"
    )

    args = parser.parse_args()

    transactions = load_transactions(args.input)

    all_frequent_itemsets = apriori(
        transactions,
        args.minsup
    )

    print_results(
        all_frequent_itemsets,
        args.input,
        args.minsup
    )


if __name__ == "__main__":
    main()
