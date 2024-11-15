import sys

def levenshtein_distance(word1, word2):
    """
    Levenshtein (Edit) Distance Dynamic Programming Algorithm
    
    Precise definition:
        Let L[i,j] be the Levenshtein distance between word1[1,2,...,i] and 
        word2[1,2,...,j]
    
    Base Cases:
        L[i,0] = i (cost to delete i characters)
        L[0,j] = j (cost to insert j characters)
    
    Solution: 
        L[|word1|, |word2|]
    
    Formula:
        L[i,j] = min{
            L[i-1,j-1] + χ(i,j),
            L[i-1,j] + 1,
            L[i,j-1] + 1
        }
        where χ(i,j) = 0 if word1[i] = word2[j]
                       1 if word1[i] ≠ word2[j]
    
    Running Time: O(|word1| × |word2|)
    """
    rows = len(word1)
    cols = len(word2)
    
    # Initialize table
    dist = [[0 for _ in range(cols + 1)] for _ in range(rows + 1)]
    
    # Base cases
    for j in range(cols + 1):
        dist[0][j] = j
    for i in range(rows + 1):
        dist[i][0] = i
        
    # Fill table
    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            if word1[i-1] == word2[j-1]:
                dist[i][j] = dist[i-1][j-1]
            else:
                dist[i][j] = 1 + min(dist[i-1][j-1], dist[i-1][j], dist[i][j-1])
    
    return dist[rows][cols]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: Requires 2 strings")
        sys.exit(1)
        
    word1, word2 = sys.argv[1], sys.argv[2]
    print(levenshtein_distance(word1, word2))