import { PubSub } from '@google-cloud/pubsub';
export const pubsub = new PubSub();
export const topicName = process.env.PUBSUB_TOPIC_NAME;
