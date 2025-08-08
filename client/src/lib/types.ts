export enum ResearchType {
    INDUSTRY_ANALYSIS = 'Industry Report',
    COMPETITOR_ANALYSIS = 'Competitor Report',
    MARKET_GAP_ANALYSIS = 'Market Gap Report',
    TARGET_MARKET_ANALYSIS = 'Target Market Report',
    BARRIER_ANALYSIS = 'Barrier Report',
    SALES_FORECASTING = 'Sales Forecast Report',
    MARKET_RESEARCH = 'Market Research Report',
}

export interface Analysis{
    _id: string;
    query: string;
    analysis_type: ResearchType;
    status: 'pending' | 'in_progress' | 'completed' | 'failed';
    created_at: string;
    report_path?: string;
}