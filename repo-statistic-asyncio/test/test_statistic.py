from app.statistics.common import Statistic
from app.statistics import (
    IssuesStatistic,
    ContributorsStatistic,
    PullRequestsStatistic,
)
from app.typehints import (
    IssueInfo,
    PRInfo,
    CommitInfo,
    _EventState,
    User,
    Commit,
    UserShort,
)
from datetime import datetime, timezone


def test_get_time_range_string():
    since = datetime(2020, 1, 1)
    until = datetime(2020, 1, 2)
    assert Statistic._get_time_range_string(
        since,
        until) == 'since 2020-01-01 until 2020-01-02'
    assert Statistic._get_time_range_string(
        since,
        None) == 'since 2020-01-01 to now'
    assert Statistic._get_time_range_string(
        None,
        until) == 'until 2020-01-02'
    assert Statistic._get_time_range_string(
        None,
        None) == 'for all time'


def test_issue_statistic():
    issues = [
        IssueInfo(
            url='some url',
            closed_at=datetime(2020, 1, 1, tzinfo=timezone.utc),
            created_at=datetime(2020, 1, 1, tzinfo=timezone.utc),
            state=_EventState.closed,
        ),
        IssueInfo(
            url='some url',
            closed_at=None,
            created_at=datetime(2020, 2, 1, tzinfo=timezone.utc),
            state=_EventState.open,
        ),
        IssueInfo(
            url='some url',
            closed_at=None,
            created_at=datetime.now(timezone.utc),
            state=_EventState.open,
        ),
    ]
    stat = IssuesStatistic(
        organisation='some org',
        repository='some repo',
        since=None,
        until=None,
        days_to_old=30,
    )
    stat.consume(issues)
    statistic = stat.get_statistic()
    assert statistic['open'] == 2
    assert statistic['closed'] == 1
    assert statistic['old'] == 1


def test_pr_statistic():
    prs = [
        PRInfo(
            url='some url',
            closed_at=datetime(2020, 1, 1, tzinfo=timezone.utc),
            created_at=datetime(2020, 1, 1, tzinfo=timezone.utc),
            state=_EventState.closed,
            draft=False,
        ),
        PRInfo(
            url='some url',
            closed_at=None,
            created_at=datetime(2020, 2, 1, tzinfo=timezone.utc),
            state=_EventState.open,
            draft=False,
        ),
        PRInfo(
            url='some url',
            closed_at=None,
            created_at=datetime.now(timezone.utc),
            state=_EventState.open,
            draft=True,
        ),
    ]
    stat = PullRequestsStatistic(
        organisation='some org',
        repository='some repo',
        since=None,
        until=None,
        days_to_old=30,
    )
    stat.consume(prs)
    statistic = stat.get_statistic()
    assert statistic['open'] == 2
    assert statistic['closed'] == 1
    assert statistic['old'] == 1


def test_contributor_statistic():
    user1 = User(login="Login1")
    user2 = User(login="Login2")
    user_short1 = UserShort(name="Name1", email="Email1")
    user_short2 = UserShort(name="Name2", email="Email2")
    commit1 = Commit(
        author=user_short1,
        committer=user_short1,
        message="Message1",
        url="Url1",
    )
    commit2 = Commit(
        author=user_short2,
        committer=user_short2,
        message="Message2",
        url="Url2",
    )
    commit3 = Commit(
        author=user_short1,
        committer=user_short1,
        message="Message3",
        url="Url3",
    )

    commits = [
        CommitInfo(
            author=user1,
            committer=user1,
            commit=commit1,
        ),
        CommitInfo(
            author=user1,
            committer=user1,
            commit=commit1,
        ),
        CommitInfo(
            author=user2,
            committer=user2,
            commit=commit2,
        ),
        CommitInfo(
            author=None,
            committer=user1,
            commit=commit3,
        ),
    ]

    stat = ContributorsStatistic(
        organisation='some org',
        repository='some repo',
        since=None,
        until=None,
        branch=None,
        top_n=15,
    )

    stat.consume(commits)
    statistic = stat.get_statistic()
    assert statistic['Login1'] == 2
    assert statistic['Login2'] == 1
    assert statistic['Name1'] == 1
