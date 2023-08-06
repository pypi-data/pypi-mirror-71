Overview
========

Provides functions to read messages from IBM Event Streams as a stream
and publish tuples to Event Streams as messages.

`IBM® Event Streams <https://www.ibm.com/cloud/event-streams>`_ is a fully managed, cloud-based messaging service.
Built on Apache Kafka, IBM Event Streams is a high-throughput, fault-tolerant, event management platform that helps 
you build intelligent, responsive, event-driven applications.

You may also review the `streamsx.kafka package <https://pypi.org/project/streamsx.kafka/>`_. to integrate 
IBM Event Streams cloud service with your IBM Streams topology applications.

Sample
======

A simple hello world example of a Streams application publishing to a topic and the same application consuming the same topic::

    from streamsx.topology.topology import Topology
    from streamsx.topology.schema import CommonSchema
    from streamsx.topology.context import submit, ContextTypes
    import streamsx.eventstreams as eventstreams
    import time

    def delay(v):
        time.sleep(5.0)
        return True

    topology = Topology('EventStreamsHelloWorld')

    to_evstr = topology.source(['Hello', 'World!'])
    to_evstr = to_evstr.as_string()
    # delay tuple by tuple
    to_evstr = to_evstr.filter(delay)

    # Publish a stream to Event Streams using HELLO topic
    eventstreams.publish(to_evstr, topic='HELLO')

    # Subscribe to same topic as a stream
    from_evstr = eventstreams.subscribe(topology, schema=CommonSchema.String, topic='HELLO')

    # You'll find the Hello World! in stdout log file:
    from_evstr.print()

    # finally submit the topology to a Streaming  Analytics Service instance
    submit(ContextTypes.STREAMING_ANALYTICS_SERVICE, topology)

Documentation
=============

* `streamsx.eventstreams package documentation <http://streamsxeventstreams.readthedocs.io/>`_


