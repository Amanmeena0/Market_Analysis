'use client'

import { Viewer, Worker } from '@react-pdf-viewer/core';
import { toolbarPlugin } from '@react-pdf-viewer/toolbar';


function PdfViewer({ url }: { url: string }) {
    const toolbarPluginInstance = toolbarPlugin();
    const { Toolbar } = toolbarPluginInstance;

    return (
        <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js">

            <div className='h-[45rem] my-4'>
                <div className="flex flex-col h-full border border-black/30">
                    {/* Toolbar row */}
                    <div className="flex items-center bg-slate-100 border-b border-black/10 px-1 py-1">
                        <Toolbar />
                    </div>

                    {/* Viewer area */}
                    <div className="flex-1 overflow-hidden">
                        <Viewer theme='dark' plugins={[toolbarPluginInstance]} fileUrl={url} />
                    </div>
                </div>
            </div>
        </Worker>
    )
}

export default PdfViewer