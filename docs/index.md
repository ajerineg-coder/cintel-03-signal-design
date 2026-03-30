# Continuous Intelligence

This site provides documentation for this project.
Use the navigation to explore module-specific materials.

## How-To Guide

Many instructions are common to all our projects.

See
[⭐ **Workflow: Apply Example**](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
to get these projects running on your machine.

## Project Documentation Pages (docs/)

- **Home** - this documentation landing page
- **Project Instructions** - instructions specific to this module
- **Your Files** - how to copy the example and create your version
- **Glossary** - project terms and concepts

## Additional Resources

- [Suggested Datasets](https://denisecase.github.io/pro-analytics-02/reference/datasets/cintel/)

## Custom Project

### Dataset
I used a system metrics dataset that includes requests, errors, and total latency values.

### Signals
I created signals for error_rate, avg_latency_ms, throughput, and a high_error_flag to identify when error rates exceed 5%.

### Experiments
I modified the original project by creating a custom Python file and adding new derived signals to better analyze system performance.

### Results
The program generated a new CSV file (signals_addie.csv) with calculated signal columns.

### Interpretation
These signals make it easier to identify performance issues. The high_error_flag helps quickly detect when the system may be experiencing problems.
