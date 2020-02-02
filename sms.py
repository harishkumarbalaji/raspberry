import nexmo

client = nexmo.Client(key='1eccfa21', secret='7E4gjWD88PgTqcl1')

client.send_message({
    'from': '919677219665',
    'to': '919677219665',
    'text': 'Alert!! Your Car is in danger!.',
})