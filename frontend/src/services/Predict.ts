import {BASE_URL} from "../utils/Config";
import type {Song} from "./SongsQuery";

export default async function Predict(trackIds: string[]): Promise<Song[]> {
    try {
        const response = await fetch(`${BASE_URL}/songs/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ track_ids: trackIds }),
        });

        if (!response.ok) {
            throw new Error(`Błąd API: ${response.status}`);
        }

        const data = await response.json();

        return data.map((song: Song) => ({
            ...song,
            img: `https://picsum.photos/seed/${song.track_id}/300`
        }));
    } catch (error) {
        console.error("Błąd podczas pobierania rekomendacji:", error);
        return [];
    }
}
