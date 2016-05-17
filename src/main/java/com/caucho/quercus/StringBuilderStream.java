package com.caucho.quercus;

import com.caucho.vfs.StreamImpl;

import java.io.IOException;

public class StringBuilderStream extends StreamImpl {
    private static StringBuilderStream _builder;
    public StringBuilder output;

    private StringBuilderStream() {
    }

    public static com.caucho.quercus.StringBuilderStream create() {
        if(_builder == null) {
            _builder = new StringBuilderStream();
            _builder.output = new StringBuilder();
        }

        return _builder;
    }

    public boolean canWrite() {
        return true;
    }

    public void write(byte[] buf, int offset, int length, boolean isEnd) throws IOException {
        String text2 = new String(buf, "ISO-8859-1");
        output.append(text2.toCharArray(),offset,length);
    }

    @Override
    public String toString() {
        return output.toString();
    }

}