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


# json_string = '{"dataType":"DiscussionFeedEventBean","majorVersion":3,"data":{"notificationReason":0,"commentId":"85cd0868-43d3-4d44-84f2-52dbb1602a68","discussionId":"1473424588801#ersynchronizer-android#dd0933eb-945e-400a-a8de-0eed1c59b087","base":{"feedEventId":"1473424588837#ersynchronizer-android#0ebdec64-1420-4874-8966-af36d824eea3","userIds":[{"userName":"ldavanzo","userEmail":"luca.davanzo@ennova-research.com","userId":"6983ff5b-1055-44f6-8916-70f11f76d150"},{"userName":"admin","userId":"800f3be4-d41e-4c53-a2f8-de97a578c46a"},{"userName":"ndefiorenze","userEmail":"nicola.defiorenze@ennova-research.com","userId":"850fcd2b-b6bc-46c3-a9e2-7e1af13c62d3"}],"reviewId":"EA-CR-1","actor":{"userName":"admin","userId":"800f3be4-d41e-4c53-a2f8-de97a578c46a"},"date":1473424588838,"reviewNumber":1},"commentText":"@{6983ff5b-1055-44f6-8916-70f11f76d150,ldavanzo} ssssssssssssss"},"minorVersion":0,"projectId":"ersynchronizer-android"}'


def discussion_feed_event_bean(param):
    print(param)
    slack_message = SlackMessage(fallback="discussion feed",
                                 color="#ff0000",
                                 text="pretext discussion_feed_event_bean",
                                 title="title",
                                 title_link="title link")
    feed_event_bean(param['base'], slack_message)
    notification_reason(param['notificationReason'], slack_message)
    if 'commentText' in param.keys():
        slack_field_comment = SlackField('Comment', param['commentText'])
        slack_message.attachments[0]['fields'].append(slack_field_comment.__dict__)
    Slack.post_to_slack(json.dumps(slack_message.__dict__))


def new_participant_in_review_feed_event_bean(param):
    print(param)


def new_revision_event_bean(param):
    pass


def participant_state_changed_feed_event_bean(param):
    pass


def pull_request_merged_feed_event_bean(param):
    pass


def removed_participant_from_review_feed_event_bean(param):
    pass


def review_created_feed_event_bean(param):
    pass


def review_state_changed_feed_event_bean(param):
    pass


def review_stopped_branch_tracking_feed_event_bean(param):
    pass


def revision_added_to_review_feed_event_bean(param):
    pass


def revision_removed_from_review_feed_event_bean(param):
    pass


def feed_event_bean(feed_event, slack_message):
    slack_message.attachments[0]['title'] = 'New comment'
    if 'userName' in feed_event['actor'].keys():
        slack_message.attachments[0]['title'] += ' by ' + feed_event['actor']['userName'];
    if 'reviewNumber' in feed_event.keys():
        slack_message.attachments[0]['text'] = 'Review number: ' + str(feed_event['reviewNumber']) + '\n';
    if 'reviewId' in feed_event.keys():
        slack_message.attachments[0]['text'] = 'Review id: ' + feed_event['reviewId'];


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
