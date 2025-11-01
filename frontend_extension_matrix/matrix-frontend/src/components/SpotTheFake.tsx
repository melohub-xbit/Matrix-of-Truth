import React, { useEffect, useState } from 'react';
import { Card, Button, Container, Grid, Typography, Box } from '@mui/material';
import { useAuth } from '../context/AuthContext'; // adjust path as needed

interface GameItem {
    id: string;
    type: 'article' | 'image' | 'audio';
    title?: string;
    url?: string;
    excerpt?: string;
}

interface GamePair {
    id: string;
    items: GameItem[];
}

interface GameAnswer {
    answer_index: number;
    explanations: string[];
}

export default function SpotTheFake() {
    const [pair, setPair] = useState<GamePair | null>(null);
    const [choice, setChoice] = useState<number | null>(null);
    const [answer, setAnswer] = useState<GameAnswer | null>(null);
    const [loading, setLoading] = useState(true);
    const { user } = useAuth();

    const fetchNewPair = async () => {
        setLoading(true);
        try {
            const res = await fetch('/api/spot-game/pair');
            const data = await res.json();
            setPair(data);
            setChoice(null);
            setAnswer(null);
        } catch (error) {
            console.error('Error fetching game pair:', error);
        }
        setLoading(false);
    };

    useEffect(() => {
        fetchNewPair();
    }, []);

    const handleVote = async (choiceIndex: number) => {
        if (!pair) return;
        
        setChoice(choiceIndex);
        
        // Submit vote
        await fetch('/api/spot-game/vote', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                pair_id: pair.id,
                choice: choiceIndex,
                user_id: user?.id || 'anonymous'
            })
        });

        // Get answer
        const res = await fetch(`/api/spot-game/answer/${pair.id}`);
        const answerData = await res.json();
        setAnswer(answerData);
    };

    if (loading) return <Box p={3}>Loading...</Box>;
    if (!pair) return <Box p={3}>No game pairs available.</Box>;

    return (
        <Container maxWidth="lg">
            <Box py={4}>
                <Typography variant="h4" gutterBottom>
                    Spot the Fake
                </Typography>
                <Typography variant="body1" paragraph>
                    Look at both items and vote which one you think is fake.
                </Typography>

                <Grid container spacing={3}>
                    {pair.items.map((item, idx) => (
                        <Grid item xs={12} md={6} key={item.id}>
                            <Card>
                                <Box p={3}>
                                    {item.type === 'image' ? (
                                        <img src={item.url} alt={item.title} style={{width: '100%'}} />
                                    ) : item.type === 'audio' ? (
                                        <audio controls src={item.url} style={{width: '100%'}} />
                                    ) : (
                                        <>
                                            <Typography variant="h6">{item.title}</Typography>
                                            <Typography variant="body1">{item.excerpt}</Typography>
                                        </>
                                    )}
                                    
                                    <Button 
                                        variant="contained"
                                        color="primary"
                                        fullWidth
                                        onClick={() => handleVote(idx)}
                                        disabled={choice !== null}
                                        sx={{ mt: 2 }}
                                    >
                                        Vote this is fake
                                    </Button>

                                    {answer && (
                                        <Box mt={2}>
                                            <Typography 
                                                color={answer.answer_index === idx ? 'error' : 'success'}
                                                variant="subtitle1"
                                            >
                                                {answer.answer_index === idx ? 
                                                    "This was indeed fake!" : 
                                                    "This was real!"
                                                }
                                            </Typography>
                                            <Typography variant="body2">
                                                {answer.explanations[idx]}
                                            </Typography>
                                        </Box>
                                    )}
                                </Box>
                            </Card>
                        </Grid>
                    ))}
                </Grid>

                <Box mt={4} textAlign="center">
                    <Button 
                        variant="outlined"
                        onClick={fetchNewPair}
                        disabled={!answer}
                    >
                        Next Pair
                    </Button>
                </Box>
            </Box>
        </Container>
    );
}