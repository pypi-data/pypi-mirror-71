# Local Emulator for Google Cloud Tasks

Google doesn't (yet) ship an emulator for the Cloud Tasks API like they do for
Cloud Datastore.

This is a stub emulator so you can run your tests and do local development without
having to connect to the production Tasks API.

**THIS IS A WORK IN PROGRESS NOT ALL API CALLS ARE COMPLETE**

## Usage

Start the emulator with:

```
gcloud-tasks-emulator start --port=9090
```

Then from within your code, use the following (instead of your normal production client connection)

### Python

```py
import grpc
from google.cloud.tasks_v2 import CloudTasksClient
from google.cloud.tasks_v2.gapic.transports.cloud_tasks_grpc_transport import CloudTasksGrpcTransport

client = CloudTasksClient(
    transport=CloudTasksGrpcTransport(channel=grpc.insecure_channel("127.0.0.1:9090"))
)
```

### Node.js

```js
const grpc = require("@grpc/grpc-js");
const { CloudTasksClient } = require('@google-cloud/tasks');

const client = new CloudTasksClient({
    servicePath: "localhost",
    port: 9090,
    sslCreds: grpc.credentials.createInsecure()
});
```

### Java

```java
import com.google.api.gax.core.NoCredentialsProvider;
import com.google.api.gax.grpc.InstantiatingGrpcChannelProvider;
import com.google.cloud.tasks.v2.CloudTasksClient;
import com.google.cloud.tasks.v2.CloudTasksSettings;
import io.grpc.ManagedChannelBuilder;

CloudTasksSettings settings = CloudTasksSettings.newBuilder()
        .setCredentialsProvider(NoCredentialsProvider.create())
        .setTransportChannelProvider(
                InstantiatingGrpcChannelProvider.newBuilder()
                        .setEndpoint("localhost:9090")
                        .setChannelConfigurator(ManagedChannelBuilder::usePlaintext)
                        .build()
        )
        .build();
CloudTasksClient client = CloudTasksClient.create(settings);
```

## The 'default' queue

By default, the emulator won't create a 'default' queue, however you can enable this
by passing the fully-qualified name of the queue:

```
gcloud-tasks-emulator start --default-queue=projects/[PROJECT]/locations/[LOCATION]/queues/default
```

## Specifying a queue.yaml

If your project uses a queue.yaml file, you can create default queues by passing its path to the `--queue-yaml` argument.

Additionally, you'll likely want to pass `--queue-yaml-project` and `--queue-yaml-location` to generate the correct
fully qualified queue names. These settings will otherwise default to `"[PROJECT]"` and `"[LOCATION]"` respectively.

## Testing
Run:
```
python gcloud_tasks_emulator/tests.py
```
