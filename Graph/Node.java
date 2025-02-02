import java.util.ArrayList;

public class Node {
    private Song valueSong;
    ArrayList<Song> songsSampledList = new ArrayList<Song>();
    int numberOfEdges;
    Node() //CONSTRUCTORS
        {valueSong = new Song();
        songsSampledList = new ArrayList<Song>(0);
        numberOfEdges = songsSampledList.size();}

    Node(Song songInput, ArrayList<Song> songsSampledListInput)
        {valueSong = songInput;
        songsSampledList = songsSampledListInput;
        numberOfEdges = songsSampledList.size();}

    public int getNumberOfEdges() { //GETTERS
        return numberOfEdges;
    }

    public ArrayList<Song> getSongsSampledList() {
        return songsSampledList;
    }
    
    public Song getValueSong() {
        return valueSong;}
    
    

    public void setSongsSampledList(ArrayList<Song> songsSampledList) { //SETTERS
        this.songsSampledList = songsSampledList;
        this.numberOfEdges = songsSampledList.size();}

    public void setValueSong(Song valueSong) {
        this.valueSong = valueSong;}


    public boolean equals(Node node2) //UTILITIES
        {return (this.valueSong.equals(node2.getValueSong()));}
    }

    

class Song{
    private String title;
    private String artist;
    private int year;

    Song(String titleInput, String artistInput, int yearInput)
        {this.title=titleInput; //SONG TITLE
         this.artist=artistInput; //ARTIST TITLE
         this.year=yearInput;} //YEAR TITLE

    Song()
        {this.title="N/A";
        this.artist="N/A";
        this.year=0;}
    


    public String getArtist() { //GETTERS
        return artist;}
    
    public String getTitle() {
        return title;}

    public int getYear() {
        return year;}
    


    public void setArtist(String artist) { //SETTERS 
        this.artist = artist;}

    public void setTitle(String title) {
        this.title = title; }

    public void setYear(int year) {
        this.year = year;}


   
     //UTILITY METHOD
    
    public String toString()
        {String returnString;
        returnString = "Song: "+title+"\n"+
                    "Artist: "+artist+"\n"+
                    "Year: "+year+"\n";
        return returnString;}
    
    public boolean equals(Song song2) {
        return (this.artist.equals(song2.getArtist()))&&(this.title.equals(song2.getTitle()))&&(this.year==song2.getYear());}
    
}


