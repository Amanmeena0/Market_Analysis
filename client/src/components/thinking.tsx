'use client'


import {  ChevronRight, LoaderPinwheel } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import Markdown from 'react-markdown';
import { Button } from './ui/button';
import { Card } from './ui/card';

function Thinking({ id }: { id: string }) {

    const [text, setText] = useState('');
    const [isError, setIsError] = useState(false);
    const [running, setRunning] = useState(false);
    const [expand, setExpand] = useState(false);
    const scrollContainerRef = useRef<HTMLDivElement>(null);

    // Auto-scroll
    useEffect(() => {
        if (scrollContainerRef.current && running) {
            scrollContainerRef.current.scrollTop = scrollContainerRef.current.scrollHeight;
        }
    }, [text, running]);


    useEffect(() => {
        setText('');
        setRunning(true);
        setIsError(false)

        //  Connect
        const ws = new WebSocket(`ws://localhost:8000/ws/research/${id}`);

        ws.onmessage = (ev) => {
            const content = ev.data;
            if (content.startsWith('__ERROR__')) {
                console.error('Error from server:', content);
                setRunning(false);
                setIsError(true);
                return;
            }
            setText((prev) => prev + content);
        };

        ws.onclose = () => {
            setRunning(false);
        };
        ws.onerror = (err) => {
            console.log(err);
            setRunning(false);
        };
        return () => {
            ws.close();
           
        };
    }, []);


    return (
        <Card className="p-8">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <h2 className="text-2xl font-bold">Creating Report</h2>
                    <div className="flex items-center gap-2">
                        <LoaderPinwheel className="animate-spin" />
                    </div>
                </div>
                <Button
                    size="icon"
                    variant="secondary"
                    onClick={() => setExpand(!expand)}
                >
                    <ChevronRight
                        className={`${expand ? 'rotate-90' : ''} transition-all duration-100`}
                    />
                </Button>
            </div>
            <div
                ref={scrollContainerRef}
                className={`p-4 rounded-2xl w-full relative text-muted-foreground text-wrap transition-all duration-300 ${expand ? 'max-h-[400px] overflow-y-auto' : 'max-h-0 overflow-hidden'}`}
            >
                <Markdown>{text}</Markdown>
            </div>

            {isError && (
                <div className="mt-4 text-red-500">
                    <h3 className="text-lg font-semibold">An error occurred:</h3>
                    <p>Please check the console for details.</p>
                </div>
            )}
        </Card>
    );
}

export default Thinking;