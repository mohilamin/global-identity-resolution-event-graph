# Metrics

## Identity Resolution Quality Score

Weighted score combining high-confidence link rate, deterministic match coverage, probabilistic match coverage, and cluster completeness.

## Match Precision Estimate

Synthetic estimate of how many resolved links are expected to be correct based on deterministic evidence and confidence thresholds.

## Match Recall Estimate

Resolved deterministic links divided by expected ground truth link count.

## Attribution Path Coverage

`attribution_path_count / conversion_event_count`

## Attribution Confidence

Starts near 0.90 and decreases with longer conversion lag and more identity-resolution dependencies.

## Fraud Risk Score

Rule-based score assigned from suspicious pattern type and involved identity count.

