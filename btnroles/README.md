You can add button reaction roles to a message by calling 

`[p]setroles <message>` where `<message>` is the message you want it to be, attach a yaml file and away you go!

An example yaml:
```yaml
Star:
  role_id: 801247649478082589
  emoji: ⭐
  style: 2
Custom Emote:
  role_id: 6192848752117123
  emoji: <:custom:634813363586859008>
  style: 2
```

The button labels are determined here by the section headings.

Only unicode and custom emotes are accepted, therefore `:smiley:` and such will not work.

