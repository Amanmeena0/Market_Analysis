"""
Market Segmentation Synthesis Task
=================================

Synthesis task for combining all research findings and creating comprehensive market segments.
"""

from crewai import Task
from prompts import TaskOutputs


class SegmentationSynthesisTask:
    """
    Market Segmentation Synthesis Task for strategic analysis and segment creation.
    
    This task involves:
    - Synthesizing multi-source research findings
    - Creating comprehensive market segments
    - Developing strategic recommendations
    - Identifying market opportunities and priorities
    """
    
    @staticmethod
    def create_task(prompts: dict, segment_synthesizer_agent, max_segments: int, context_tasks: list):
        """
        Create the segmentation synthesis task.
        
        Args:
            prompts: Dictionary containing formatted prompts
            segment_synthesizer_agent: The segment synthesizer agent instance
            max_segments: Maximum number of segments to create
            context_tasks: List of previous tasks to use as context
            
        Returns:
            Configured CrewAI Task instance
        """
        return Task(
            description=prompts['segmentation_synthesis'],
            agent=segment_synthesizer_agent,
            expected_output=TaskOutputs.get_segmentation_output(max_segments),
            context=context_tasks
        )
