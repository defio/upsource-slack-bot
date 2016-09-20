import json
from app import Slack
from app.SlackField import SlackField
from flask import Flask, render_template, request, jsonify

# Initialize the Flask application
from app.SlackMessage import SlackMessage

app = Flask(__name__)


@app.route('/')
def index():
    # Render template
    return render_template('index.html')


@app.route('/post', methods=['POST'])
def post():
    # Get the parsed contents of the form data
    json = request.json
    print(request.json)
    try:
        dataType = json['dataType']

        baseMessages = {'DiscussionFeedEventBean': discussion_feed_event_bean,
                        'NewParticipantInReviewFeedEventBean': new_participant_in_review_feed_event_bean,
                        'NewRevisionEventBean': new_revision_event_bean,
                        'ParticipantStateChangedFeedEventBean': participant_state_changed_feed_event_bean,
                        'PullRequestMergedFeedEventBean': pull_request_merged_feed_event_bean,
                        'RemovedParticipantFromReviewFeedEventBean': removed_participant_from_review_feed_event_bean,
                        'ReviewCreatedFeedEventBean': review_created_feed_event_bean,
                        'ReviewStateChangedFeedEventBean': review_state_changed_feed_event_bean,
                        'ReviewStoppedBranchTrackingFeedEventBean': review_stopped_branch_tracking_feed_event_bean,
                        'RevisionAddedToReviewFeedEventBean': revision_added_to_review_feed_event_bean,
                        'RevisionRemovedFromReviewFeedEventBean': revision_removed_from_review_feed_event_bean,
                        }

        baseMessages[dataType](json['data'])
    except KeyError:
        print('dataType not found')

    return jsonify(json)


def discussion_feed_event_bean(param):
    slack_message = SlackMessage(fallback="discussion feed",
                                 color="#ff0000",
                                 text="pretext discussion_feed_event_bean",
                                 title="title",
                                 title_link="title link")
    slack_message.attachments[0]['title'] = 'New comment'
    feed_event_bean(param['base'], slack_message)
    notification_reason(param['notificationReason'], slack_message)
    if 'commentText' in param.keys():
        slack_field_comment = SlackField('Comment', param['commentText'])
        slack_message.attachments[0]['fields'].append(slack_field_comment.__dict__)
    Slack.post_to_slack(json.dumps(slack_message.__dict__))


def new_participant_in_review_feed_event_bean(param):
    slack_message = SlackMessage(fallback="new participant in review",
                                 color="#FF9751",
                                 text="new_participant_in_review_feed_event_bean",
                                 title="new participant in review",
                                 title_link="title link")
    slack_message.attachments[0]['title'] = 'New comment'
    if 'reviewId' in param['base'].keys():
        slack_message.attachments[0]['text'] = 'Review id: ' + param['base']['reviewId'];
    user_id_bean(param['participant'], slack_message)
    slack_message.attachments[0]['title'] += " was added to review"
    slack_message.attachments[0]['text'] = 'With role: ' + participant_role(param['role'])
    Slack.post_to_slack(json.dumps(slack_message.__dict__))


def new_revision_event_bean(param):
    pass


def participant_state_changed_feed_event_bean(param):
    slack_message = SlackMessage(fallback="participant state changed",
                                 color="#F39751",
                                 text="participant_state_changed_feed_event_bean",
                                 title="participant state changed",
                                 title_link="title link")
    if 'reviewId' in param['base'].keys():
        slack_message.attachments[0]['text'] = 'Review id: ' + param['base']['reviewId'];
    user_id_bean(param['participant'], slack_message)
    slack_message.attachments[0]['title'] += " change state"
    participant_role(param['role'], slack_message)
    Slack.post_to_slack(json.dumps(slack_message.__dict__))


def pull_request_merged_feed_event_bean(param):
    pass


def removed_participant_from_review_feed_event_bean(param):
    pass


def review_created_feed_event_bean(param):
    slack_message = SlackMessage(fallback="review created",
                                 color="#ffcc00",
                                 text="pretext review_created_feed_event_bean",
                                 title="title",
                                 title_link="title link")
    feed_event_bean(param['base'], slack_message)
    slack_message.attachments[0]['title'] = 'New review created'
    Slack.post_to_slack(json.dumps(slack_message.__dict__))


def review_state_changed_feed_event_bean(param):
    slack_message = SlackMessage(fallback="review state changed",
                                 color="#400F63",
                                 text="pretext review_state_changed_feed_event_bean",
                                 title="title",
                                 title_link="title lin  k")
    slack_message.attachments[0]['title'] = 'review state changed'
    feed_event_bean(param['base'], slack_message)
    slack_field_state_changed = SlackField(
        "Status changed from \'%s\' to \'%s\' " % (review_state(param['oldState']), review_state(param['newState'])),
        "")
    slack_message.attachments[0]['fields'].append(slack_field_state_changed.__dict__)
    Slack.post_to_slack(json.dumps(slack_message.__dict__))


def review_state(state):
    if state == 0:
        return "Open"
    elif state == 1:
        return "Closed"
    else:
        return "Unknown"


def review_stopped_branch_tracking_feed_event_bean(param):
    pass


def revision_added_to_review_feed_event_bean(param):
    pass


def revision_removed_from_review_feed_event_bean(param):
    pass


def feed_event_bean(feed_event, slack_message):
    if 'userName' in feed_event['actor'].keys():
        slack_message.attachments[0]['title'] += ' by ' + feed_event['actor']['userName'];
    if 'reviewNumber' in feed_event.keys():
        slack_message.attachments[0]['text'] = 'Review number: ' + str(feed_event['reviewNumber']) + '\n';
    if 'reviewId' in feed_event.keys():
        slack_message.attachments[0]['text'] = 'Review id: ' + feed_event['reviewId'];


def user_id_bean(user_id, slack_message):
    if 'userName' in user_id.keys():
        slack_message.attachments[0]['title'] = user_id['userName'] ;


def participant_role(role):
    if role == 1:
        return ' Author';
    elif role == 2:
        return ' Reviewer';
    elif role == 3:
        return ' Watcher';


def notification_reason(param, slack_message):
    to_append = '';
    if param == 0:
        # to_append = 'Unknown'
        pass
    elif param == 1:
        to_append = 'CommentInAuthorFeed'
    elif param == 2:
        to_append = 'NotifyCommitAuthor'
    elif param == 3:
        to_append = 'Mention'
    elif param == 4:
        to_append = 'HashTagSubscription'
    elif param == 5:
        to_append = 'DiscussionIsStarred'
    elif param == 6:
        to_append = 'ParticipatedInDiscussion'
    elif param == 7:
        to_append = 'ParticipatedInReview'
    elif param == 8:
        to_append = 'Reply'
    slack_message.attachments[0]['title'] += ' ' + to_append;
