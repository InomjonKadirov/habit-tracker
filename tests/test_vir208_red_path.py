"""Deliberately failing test — VIR-208 P2-4 live proof. Delete after the proof.

Exists to make this repository's GitHub Actions workflow fail on purpose, so a
failed run's job log can be traced end to end: out of the Actions job, through
`utils.github_client.failed_job_logs`, and into the coding agent's retry prompt.

The assertion message carries a marker string that appears nowhere else in this
repository or in VirtuAgent. Finding it downstream is therefore proof the log
was really fetched and forwarded, not that some other code path produced a
plausible-looking failure message of its own.
"""


def test_vir208_red_path_marker():
    marker = "VIR208-RED-PATH-MARKER-8f3a1c"
    assert False, f"{marker}: deliberate failure proving the Actions job log reaches the agent"
