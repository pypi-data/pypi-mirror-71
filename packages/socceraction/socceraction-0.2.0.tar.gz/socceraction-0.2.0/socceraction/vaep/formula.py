import pandas as pd  # type: ignore


def _prev(x: pd.Series) -> pd.Series:
    prev_x = x.shift(1)
    prev_x[:1] = x.values[0]
    return prev_x


_samephase_nb: int = 10


def offensive_value(
    actions: pd.DataFrame, scores: pd.Series, concedes: pd.Series
) -> pd.Series:
    sameteam = _prev(actions.team_id) == actions.team_id
    prev_scores = _prev(scores) * sameteam + _prev(concedes) * (~sameteam)

    # if the previous action was too long ago, the odds of scoring are now 0
    toolong_idx = (
        abs(actions.time_seconds - _prev(actions.time_seconds)) > _samephase_nb
    )
    prev_scores[toolong_idx] = 0

    # if the previous action was a goal, the odds of scoring are now 0
    prevgoal_idx = (
        _prev(actions.type_name).isin(["shot", "shot_freekick", "shot_penalty"])
    ) & (_prev(actions.result_name) == "success")
    prev_scores[prevgoal_idx] = 0

    # fixed odds of scoring when penalty
    penalty_idx = actions.type_name == "shot_penalty"
    prev_scores[penalty_idx] = 0.792453

    # fixed odds of scoring when corner
    corner_idx = actions.type_name.isin(["corner_crossed", "corner_short"])
    prev_scores[corner_idx] = 0.046500

    return scores - prev_scores


def defensive_value(
    actions: pd.DataFrame, scores: pd.Series, concedes: pd.Series
) -> pd.Series:
    sameteam = _prev(actions.team_id) == actions.team_id
    prev_concedes = _prev(concedes) * sameteam + _prev(scores) * (~sameteam)

    toolong_idx = (
        abs(actions.time_seconds - _prev(actions.time_seconds)) > _samephase_nb
    )
    prev_concedes[toolong_idx] = 0

    # if the previous action was a goal, the odds of conceding are now 0
    prevgoal_idx = (
        _prev(actions.type_name).isin(["shot", "shot_freekick", "shot_penalty"])
    ) & (_prev(actions.result_name) == "success")
    prev_concedes[prevgoal_idx] = 0

    return -(concedes - prev_concedes)


def value(
    actions: pd.DataFrame, Pscores: pd.Series, Pconcedes: pd.Series
) -> pd.DataFrame:
    v = pd.DataFrame()
    v["offensive_value"] = offensive_value(actions, Pscores, Pconcedes)
    v["defensive_value"] = defensive_value(actions, Pscores, Pconcedes)
    v["vaep_value"] = v["offensive_value"] + v["defensive_value"]
    return v
