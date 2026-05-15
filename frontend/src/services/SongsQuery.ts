import {BASE_URL} from "../utils/Config";

export interface Song {
    id: number;
    track_id: string;
    artists: string;
    album_name: string;
    track_name: string;
    popularity: number;
    duration_ms: number;
    explicit: boolean;
    danceability: number;
    energy: number;
    key: number;
    loudness: number;
    mode: number;
    speechiness: number;
    acousticness: number;
    instrumentalness: number;
    liveness: number;
    valence: number;
    tempo: number;
    time_signature: number;
    track_genre: string;
}

export default async function searchSongs(name: string): Promise<Song[]> {
    try {
        const response = await fetch(`${BASE_URL}/songs/search/${encodeURIComponent(name)}`);
        
        if (!response.ok) {
            if (response.status === 404) return [];
            throw new Error(`Błąd API: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Błąd podczas wyszukiwania piosenek:", error);
        return [];
    }
}
