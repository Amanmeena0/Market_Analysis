'use client'

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardFooter, CardHeader } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ResearchType } from "@/lib/types";
import { Dot, SparklesIcon } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function Home() {
  const [query, setquery] = useState("");
  const [analysisType, setAnalysisType] = useState("");
  const [loading, setloading] = useState(false);
  const [queryerror, setqueryerror] = useState("");
  const [analysiserror, setanalysiserror] = useState("");

  const router = useRouter()

  async function handleSubmit() {

    if (!query) {
      setqueryerror("Please enter a market topic to research");
    }

    if (!analysisType) {
      setanalysiserror("Please select an analysis type");
    }

    if (!query || !analysisType) {
      return;
    }

    setqueryerror("");
    setanalysiserror("");
    setloading(true);

    try {

      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/analysis`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          analysis_type: analysisType,
        }),
      })

      if (!res.ok) {
        console.error("Failed to create analysis:", res.statusText);
        setloading(false);
        return;
      }
      const { id } = await res.json();
      router.push(`/analysis/${id}`)

    } catch (error) {
      setloading(false);
      console.log(error)
    }


  }



  return (
    <main className="container h-full w-full space-y-4 ">
      <div className="flex flex-col items-center justify-center gap-4 sm:gap-6 p-4">
        <h1 className="text-center text-3xl sm:text-5xl font-bold  text-nowrap text-primary">Market Research Platform</h1>
        <p className="text-2xl text-center lg:max-w-1/2  text-muted-foreground">Leverage AI-powered analytics to gain comprehensive market insights and make data-driven business decisions</p>
      </div>

      <Card className="lg:w-[50%] sm:w-[70%] mx-auto max-sm:w-[90%]">
        <CardHeader className="text-center ">
          <Badge variant={'outline'} className="text-md mb-2 bg-primary/5 text-primary mx-auto space-x-2 p-2 px-4 rounded-full">
            <SparklesIcon />
            <p>AI-Powered Analysis</p>
          </Badge>
          <h2 className="text-3xl font-semibold">What market would you like to research?</h2>
          <p className="text-muted-foreground">Enter a topic and we&apos;ll provide comprehensive market insights</p>
        </CardHeader>
        <CardDescription className="px-8 space-y-4">
          <div className="space-y-1">

            {queryerror && <p className="text-xs text-red-500">{queryerror}</p>}
            <Input value={query} onChange={(e) => setquery(e.target.value)} placeholder="Enter a market topic..." className="h-12" />
          </div>
          <div className="space-y-1">
            {analysiserror && <p className="text-xs text-red-500">{analysiserror}</p>}
            <Select value={analysisType} onValueChange={setAnalysisType}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Analysis Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={ResearchType.INDUSTRY_ANALYSIS}>Industry Analysis</SelectItem>
                <SelectItem value={ResearchType.MARKET_GAP_ANALYSIS}>Market Gap Analysis</SelectItem>
                <SelectItem value={ResearchType.COMPETITOR_ANALYSIS}>Competitor Analysis</SelectItem>
                <SelectItem value={ResearchType.BARRIER_ANALYSIS}>Barrier Analysis</SelectItem>
                <SelectItem value={ResearchType.TARGET_MARKET_ANALYSIS}>Target Market Segmentation</SelectItem>
                <SelectItem value={ResearchType.SALES_FORECASTING}>Sales Forecasting</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <Button disabled={loading} className="w-full h-10 text-xl text-primary-foreground" onClick={handleSubmit}>
            {!loading && <p>Analyse Market</p>}
            {loading && <div className="flex gap-0">
              <Dot className={`h-8 w-8 -mx-2 animate-bounce delay-0`} />
              <Dot className={`h-8 w-8 -mx-2 animate-bounce delay-150`} />
              <Dot className={`h-8 w-8 -mx-2 animate-bounce delay-300`} />
            </div>}
          </Button>
        </CardDescription>
        <CardFooter className="space-y-4 block">
          <p className="text-muted-foreground text-center w-full">Popular Search Topics:</p>
          <div className="flex flex-wrap justify-center gap-2">
            <Button variant={'outline'} onClick={() => setquery('Electric vehicle market')}>Electric vehicle market</Button>
            <Button variant={'outline'} onClick={() => setquery('AI in healthcare')}>AI in healthcare</Button>
            <Button variant={'outline'} onClick={() => setquery('Sustainable Fashion')}>Sustainable Fashion</Button>
            <Button variant={'outline'} onClick={() => setquery('Remote work Software')}>Remote work Software</Button>
            <Button variant={'outline'} onClick={() => setquery('Plant based food industry')}>Plant based food industry</Button>
          </div>
        </CardFooter>
      </Card>
    </main>
  );
}
