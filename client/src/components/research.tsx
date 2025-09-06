'use client'

import { Viewer, Worker } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css';
import { toolbarPlugin } from '@react-pdf-viewer/toolbar';
import '@react-pdf-viewer/toolbar/lib/styles/index.css';
import { ChevronDown, LoaderPinwheel } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import Markdown from 'react-markdown';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { ResearchType } from '@/lib/types';

function Research({ rtype }: { rtype: ResearchType }) {

    const toolbarPluginInstance = toolbarPlugin();
    const { Toolbar } = toolbarPluginInstance;

    const [text, setText] = useState('');
    const [query, setQuery] = useState('');
    const [isError, setIsError] = useState(false);
    const [expand, setExpand] = useState(false);
    const [running, setRunning] = useState(false);
    const [elapsedTime, setElapsedTime] = useState(0);
    const [isDone, setIsDone] = useState(false);
    const [rid, setRid] = useState("");
    const scrollContainerRef = useRef<HTMLDivElement>(null);
    const wsRef = useRef<WebSocket | null>(null);
    const timerRef = useRef<NodeJS.Timeout | null>(null);

    // Auto-scroll
    useEffect(() => {
        if (scrollContainerRef.current && running) {
            scrollContainerRef.current.scrollTop = scrollContainerRef.current.scrollHeight;
        }
    }, [text, running]);

    // Timer effect
    useEffect(() => {
        if (running) {
            setElapsedTime(0);
            timerRef.current = setInterval(() => {
                setElapsedTime(prev => prev + 1);
            }, 1000);
        } else {
            if (timerRef.current) {
                clearInterval(timerRef.current);
                timerRef.current = null;
            }
        }

        return () => {
            if (timerRef.current) {
                clearInterval(timerRef.current);
            }
        };
    }, [running]);

    // Kill the socket when the component unmounts
    useEffect(() => {
        return () => {
            wsRef.current?.close();
            if (timerRef.current) {
                clearInterval(timerRef.current);
            }
        };
    }, []);

    // Format elapsed time as MM:SS
    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    };

    // -----------------------------------------------------------------
    // Core handler: POST to /ws/start then open WebSocket
    // -----------------------------------------------------------------
    const startResearch = async () => {
        setText('');
        setRunning(true);
        setIsError(false)
        setIsDone(false)

        // 1. Start the job
        const { request_id } = await fetch('http://localhost:8000/ws/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_prompt: query }),
        }).then((r) => r.json());

        setRid(request_id);

        // 2. Connect
        const ws = new WebSocket(`ws://localhost:8000/ws/research/${request_id}`);
        wsRef.current = ws;

        ws.onmessage = (ev) => {
            const content = ev.data;
            if (content.startsWith('__ERROR__')) {
                console.error('Error from server:', content);
                setRunning(false);
                setIsDone(false);
                setIsError(true);
                return;
            }
            setText((prev) => prev + content);
        };

        ws.onclose = () => {
            setIsDone(true)
            setRunning(false);
        };
        ws.onerror = (err) => {
            console.log(err);
            setRunning(false);
        };
    };



    return (
        <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js">

            <div className="p-8">
                <Card>
                    <CardHeader>
                        {running ? (
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <h2 className="text-2xl font-bold">Thinking</h2>
                                    <div className="flex items-center gap-2">
                                        <LoaderPinwheel className="animate-spin" />
                                        <span className="text-sm font-mono  px-2 py-1 rounded">
                                            {formatTime(elapsedTime)}
                                        </span>
                                    </div>
                                </div>
                                <Button
                                    size="icon"
                                    variant="secondary"
                                    onClick={() => setExpand(!expand)}
                                >
                                    <ChevronDown
                                        className={`${expand ? '-rotate-90' : ''} transition-all duration-100`}
                                    />
                                </Button>
                            </div>
                        ) : (
                            <div className="flex gap-8 items-center">
                                <Label htmlFor="query" className="text-4xl font-thin">
                                    Query
                                </Label>
                                <Input
                                    value={query}
                                    onChange={(e) => setQuery(e.target.value)}
                                    id="query"
                                    className="h-12"
                                    placeholder="Type your query..."
                                />
                            </div>
                        )}
                    </CardHeader>

                    <CardContent className="rounded-2xl">
                        {!running || isDone ? (
                            <Button
                                onClick={startResearch}
                                className="w-full h-12 bg-blue-500 text-white hover:bg-blue-600 transition-colors"
                            >
                                Start Research
                            </Button>
                        ) : (
                            <div
                                ref={scrollContainerRef}
                                className={`p-4 rounded-2xl w-full relative text-primary/50 text-wrap transition-all duration-300
                ${expand ? 'h-96 overflow-y-auto' : 'max-h-32 overflow-scroll'}`}
                            >
                                <Markdown>{text}</Markdown>
                            </div>
                        )}
                    </CardContent>
                </Card>
                {isError && (
                    <div className="mt-4 text-red-500">
                        <h3 className="text-lg font-semibold">An error occurred:</h3>
                        <p>Please check the console for details.</p>
                    </div>
                )}

                {isDone && !isError && <div className='h-[40rem] my-4'>
                    <div className="flex flex-col h-full border border-black/30">
                        {/* Toolbar row */}
                        <div className="flex items-center bg-slate-100 border-b border-black/10 px-1 py-1">
                            <Toolbar />
                        </div>

                        {/* Viewer area */}
                        <div className="flex-1 overflow-hidden">
                            <Viewer theme='dark' plugins={[toolbarPluginInstance]} fileUrl={`${process.env.NEXT_PUBLIC_API_URL}/reports/${rid}/${rtype.toString()}.pdf`} />
                        </div>
                    </div>
                </div>
                }
            </div>
        </Worker>
    );
}

export default Research;