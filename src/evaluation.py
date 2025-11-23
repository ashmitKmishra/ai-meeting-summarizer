"""
Evaluation Module - Metrics and Comparison
Member 3: Data Scientist (Baseline)
File Ownership: src/baseline.py, src/evaluation.py

Compare AI results with regex baseline
"""

from typing import Dict, List
import json


def compare_results(ai_json: Dict, regex_list: List) -> Dict:
    """
    Compare AI-generated results with regex baseline
    
    Args:
        ai_json (dict): Results from AI pipeline (Whisper + Gemini)
        regex_list (list): Results from regex baseline
    
    Returns:
        dict: Comparison metrics including:
            - precision
            - recall
            - f1_score
            - common_items
            - ai_only_items
            - regex_only_items
    
    TODO: Implement comparison metrics:
    - Calculate precision, recall, F1 score
    - Find overlapping action items
    - Analyze differences
    - Generate comparison report
    """
    
    ai_items = set(ai_json.get('action_items', []))
    regex_items = set(regex_list)
    
    common = ai_items.intersection(regex_items)
    ai_only = ai_items - regex_items
    regex_only = regex_items - ai_items
    
    # Calculate metrics
    precision = len(common) / len(ai_items) if ai_items else 0
    recall = len(common) / len(regex_items) if regex_items else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'metrics': {
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score
        },
        'common_items': list(common),
        'ai_only_items': list(ai_only),
        'regex_only_items': list(regex_only),
        'total_ai_items': len(ai_items),
        'total_regex_items': len(regex_items),
        'total_common': len(common)
    }


def evaluate_summary_quality(ai_summary: str, reference_summary: str) -> Dict:
    """
    Evaluate quality of AI-generated summary
    
    Args:
        ai_summary: AI-generated summary
        reference_summary: Reference/ground truth summary
    
    Returns:
        dict: Quality metrics
    """
    # TODO: Implement quality metrics
    # - ROUGE scores
    # - BLEU scores
    # - Length comparison
    # - Keyword overlap
    
    return {
        'rouge_score': 0.0,
        'bleu_score': 0.0,
        'length_ratio': len(ai_summary) / len(reference_summary) if reference_summary else 0
    }


def generate_comparison_report(comparison_data: Dict) -> str:
    """
    Generate a human-readable comparison report
    
    Args:
        comparison_data: Results from compare_results()
    
    Returns:
        str: Formatted report
    """
    report = []
    report.append("=" * 60)
    report.append("AI vs Regex Baseline Comparison Report")
    report.append("=" * 60)
    
    metrics = comparison_data['metrics']
    report.append(f"\nMetrics:")
    report.append(f"  Precision: {metrics['precision']:.2%}")
    report.append(f"  Recall: {metrics['recall']:.2%}")
    report.append(f"  F1 Score: {metrics['f1_score']:.2%}")
    
    report.append(f"\nItem Counts:")
    report.append(f"  AI Items: {comparison_data['total_ai_items']}")
    report.append(f"  Regex Items: {comparison_data['total_regex_items']}")
    report.append(f"  Common Items: {comparison_data['total_common']}")
    
    return "\n".join(report)
