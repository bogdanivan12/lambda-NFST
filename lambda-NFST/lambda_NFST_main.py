"""Main module for lambda_NFST project"""
from typing import List


def read(input_file_path: str):
    """Reads the input file and returns the contents as a list of strings"""
    with open(input_file_path, "r") as file:
        return file.readlines()


def transform_input_into_nfst(input_data: list):
    """Transforms the input data into a NFST"""
    adjacency_list = {}
    no_of_states, no_of_transitions = [int(x) for x in input_data[0].split()]
    for i in range(1, no_of_transitions + 1):
        state1, state2, *transition = input_data[i].split()
        transition = tuple(transition)
        if state1 not in adjacency_list:
            adjacency_list[state1] = {
                state2: []
            }
        if state2 not in adjacency_list[state1]:
            adjacency_list[state1][state2] = []
        adjacency_list[state1][state2].append(transition)
    initial_state = input_data[no_of_transitions + 1].strip()
    final_states = input_data[no_of_transitions + 2].split()
    return (
        no_of_states,
        no_of_transitions,
        adjacency_list,
        initial_state,
        final_states
    )


def get_words_from_input(input_data: list, no_of_transitions: int):
    """Returns the words to be translated from the input data"""
    no_of_words = int(input_data[no_of_transitions + 3])
    words_list = [
        x.strip() for x in
        input_data[no_of_transitions + 4: no_of_transitions + 4 + no_of_words]
    ]
    return no_of_words, words_list


def dfs(adjacency_list: dict, final_states: List[str], word: str, state: str,
        translated_word: str=""):
    """Performs a depth-first search on the NFST"""
    if not word:
        if state in final_states:
            print(translated_word)
        return
    for neighbour in adjacency_list[state]:
        for transition in adjacency_list[state][neighbour]:
            if transition[0] == word[0] or transition[0] == "#":
                dfs(
                    adjacency_list=adjacency_list,
                    final_states=final_states,
                    word=word[1:],
                    state=neighbour,
                    translated_word=(
                        f"{translated_word}"
                        f"{transition[1] if transition[1] != '#' else ''}"
                    )
                )


def main():
    """
        Main function that reads the NFST from the input file and the given
        words and translates them based on the rules of the NFST
    """
    input_data = read("../input/input.txt")
    (
        no_of_states,
        no_of_transitions,
        adjacency_list,
        initial_state,
        final_states
    ) = transform_input_into_nfst(input_data)
    no_of_words, words_list = get_words_from_input(
        input_data=input_data,
        no_of_transitions=no_of_transitions
    )
    for word in words_list:
        print(f"{word} -> ", end="")
        dfs(
            adjacency_list=adjacency_list,
            final_states=final_states,
            word=word,
            state=initial_state,
            translated_word=""
        )

if __name__ == "__main__":
    main()
