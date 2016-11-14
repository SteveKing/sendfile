function sendfile ()
{
    echo '-*-{{SENDFILE}}-*-';
    echo "{\"version\": 1.0, \"host\": \"`hostname`\"}";
    env COPYFILE_DISABLE=true tar czf - "$@" 2> /dev/null | base64;
    echo '-*-{{DONE}}-*-'
}
