import PdfViewer from '@/components/pdf-viewer';
import Thinking from '@/components/thinking';
import { Card, CardDescription, CardHeader } from '@/components/ui/card';
import { Analysis } from '@/lib/types';

async function AnalysisPage({ params }: { params: Promise<{ id: string }> }) {
    const { id } = await params;
    
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/analysis/${id}`, {
        method: 'GET',
    });

    if (!res.ok) {
        console.error("Failed to fetch analysis:", res.statusText);
        return;
    }

    const data = await res.json() as Analysis;

    return (
        <main className='container space-y-6 h-full py-8'>
            <Card className='-space-y-4'>
                <CardHeader className='flex justify-between items-center gap-4'>
                    <div className='flex gap-2 items-center text-2xl' >
                        <p>Analysis Status :</p>
                        <span className='text-primary font-semibold capitalize'>{data.status}</span>
                    </div>
                    <div>
                        <p className='text-end text-lg text-muted-foreground'>Created At:</p>
                        <p>{new Date(data.created_at).toLocaleString('en-US', {
                            year: 'numeric',
                            month: 'short',
                            day: 'numeric',
                            hour: 'numeric',
                            minute: '2-digit',
                            hour12: true
                        })}</p>
                    </div>

                </CardHeader>
                <CardDescription className='px-6 text-lg'>
                    <p>{data.query}</p>
                    <p className='text-muted-foreground font-semibold'>Type: {data.analysis_type}</p>
                </CardDescription>

            </Card>
            {data.status === 'pending' && (
                <Thinking id={data._id} />
            )}
            {data.status == 'completed' && <PdfViewer url={`${process.env.NEXT_PUBLIC_API_URL}/reports/${data.report_path}`} />}
        </main>
    )
}

export default AnalysisPage