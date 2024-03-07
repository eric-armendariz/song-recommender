import pandas as pd
from pathlib import Path
import scipy
from implicit.datasets.lastfm import get_lastfm

#Load user artists file and return a csr matrix
#file_path: path to user artist file
#output contains userID, artistID and weight
def load_user_artists(file_path: Path) -> scipy.sparse.csr_matrix:
    user_artists = pd.read_csv(file_path, sep="\t")
    user_artists.set_index(["userID", "artistID"], inplace=True)
    coo = scipy.sparse.coo_matrix(
        (
            user_artists.weight.astype(float),
            (
                user_artists.index.get_level_values(0),
                user_artists.index.get_level_values(1),
            ),
        )
    )
    
    return coo.tocsr()

#Class to help get artistName from artistID
class ArtistRetriever:
    def __init__(self):
        self.artist_df = None

    #Returns artist name from artist ID
    def get_artist_name_from_id(self, artist_id: int) -> str:
        return self.artist_df.loc[artist_id-1, "name"]

    #Loads artist to id file into class dataframe
    def load_artists(self, artists_file: Path) -> None:
        artists_df = pd.read_csv(artists_file, sep="\t")
        artists_df.set_index("id")
        self.artist_df = artists_df
        print(self.artist_df)
    

def main():
    user_artists = load_user_artists("Dataset/user_artists.dat")

    artistRetriever = ArtistRetriever()
    artistRetriever.load_artists("Dataset/artists.dat")
    artist = artistRetriever.get_artist_name_from_id(1)
    print(artist)

if __name__ == "__main__":
    main()
