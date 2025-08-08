'use client'


import { ChevronRight, LoaderPinwheel } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import Markdown from 'react-markdown';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { useRouter } from 'next/navigation';

function Thinking({ id }: { id: string }) {

    const [text, setText] = useState('');
    const [isError, setIsError] = useState(false);
    const [running, setRunning] = useState(false);
    const [expand, setExpand] = useState(false);
    const scrollContainerRef = useRef<HTMLDivElement>(null);
    const router = useRouter()

    // Auto-scroll to bottom when new text is added
    useEffect(() => {
        if (scrollContainerRef.current && expand) {
            scrollContainerRef.current.scrollTop = scrollContainerRef.current.scrollHeight;
        }
    }, [text, expand]);


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
            if (content.startsWith('__OUTPUT_FILE__')) {
                console.log('File output:', content);
                router.refresh();
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
                    {running && (
                        <div className="flex items-center gap-2">
                            <LoaderPinwheel className="animate-spin" />
                        </div>
                    )}
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
                className={`p-4 rounded-2xl w-full relative text-muted-foreground transition-all duration-300 ${expand ? 'max-h-[600px] overflow-y-auto' : 'max-h-0 overflow-hidden'}`}
            >
                <div className="prose prose-sm max-w-none break-words overflow-wrap-anywhere">
                    <Markdown 
                        components={{
                            p: ({ children }) => <p className="break-words whitespace-pre-wrap">{children}</p>,
                            div: ({ children }) => <div className="break-words">{children}</div>,
                            span: ({ children }) => <span className="break-words">{children}</span>,
                            code: ({ children }) => <code className="break-all bg-background px-1 py-0.5 rounded text-xs">{children}</code>,
                            pre: ({ children }) => <pre className="break-all overflow-x-auto whitespace-pre-wrap bg-background p-2 rounded">{children}</pre>
                        }}
                    >
                        {text}
                    </Markdown>
                </div>
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